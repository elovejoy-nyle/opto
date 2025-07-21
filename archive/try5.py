import time
import pathlib
import urllib3
import requests
from bs4 import BeautifulSoup
from scapy.all import sniff, Ether, get_if_hwaddr

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Suppress SSL warnings ---
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# === SETTINGS ===
interface_name = "Ethernet 4"  # Change to match your environment
username = "nyle"
password = "nyle1234"
backup_file_path = "models/E360/e360_groov-rio-backup_1_2.zip"

# === SCAPY: MAC SNIFFING ===
def get_peer_mac(interface):
    my_mac = get_if_hwaddr(interface).lower()
    def stop_on_peer(pkt):
        return Ether in pkt and pkt[Ether].src.lower() != my_mac
    packets = sniff(iface=interface, stop_filter=stop_on_peer, timeout=10)
    for pkt in packets:
        if Ether in pkt:
            src = pkt[Ether].src.lower()
            if src != my_mac:
                return src
    return None

def format_opto(mac):
    parts = mac.lower().split(":")[-3:]
    return f"opto-{parts[0]}-{parts[1]}-{parts[2]}"

def create_opto_user(hostname, username, password):
    base_url = f"https://{hostname}"
    session = requests.Session()

    # Step 1: Load the commissioning form to get CSRF token
    page = session.get(f"{base_url}/commissioning/start.html", verify=False)
    soup = BeautifulSoup(page.text, "html.parser")
    csrf = soup.find("input", {"name": "csrf"})
    if not csrf:
        print("[!] CSRF token not found.")
        return False
    csrf_token = csrf["value"]

    # Step 2: Submit the account creation form
    form_data = {
        "uname": username,
        "pwd": password,
        "confirmPwd": password,
        "csrf": csrf_token
    }
    post_url = f"{base_url}/auth/access/user/commission/form"
    resp = session.post(post_url, data=form_data, verify=False)

    if resp.status_code == 200 and "error" not in resp.text.lower():
        print("[+] Account created successfully.")
        return True
    else:
        print("[!] Account creation failed.")
        return False

# === MAIN SCRIPT ===
rio_mac = get_peer_mac(interface_name)
if not rio_mac:
    print("[!] No peer MAC address detected.")
    exit(1)

hostname = format_opto(rio_mac)
print(f"[+] Device hostname: {hostname}")

# --- Create user if needed ---
create_opto_user(hostname, username, password)

# --- Selenium: Automate upload ---
print("[*] Launching browser...")
firefox_options = Options()
firefox_options.set_preference("dom.webnotifications.enabled", False)

driver = webdriver.Firefox(options=firefox_options)
driver.get(f"https://{hostname}/login/")
driver.maximize_window()

# --- Login ---
print("[*] Logging in...")
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "uname")))
driver.find_element(By.NAME, "uname").send_keys(username)
driver.find_element(By.NAME, "pwd").send_keys(password)
driver.find_element(By.CLASS_NAME, "btn-primary").click()

# --- Wait for dashboard redirect ---
WebDriverWait(driver, 30).until(EC.url_contains("/manage"))

# --- Navigate to restore page ---
print("[*] Navigating to restore page...")
driver.get(f"https://{hostname}/manage/local/system/restore")

# --- Wait for file input ---
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "backup")))

# --- Upload the ZIP file ---
print("[*] Uploading backup file...")
abs_path = str(pathlib.Path(backup_file_path).resolve())
driver.find_element(By.NAME, "backup").send_keys(abs_path)

# --- Wait and click "Restore and Restart" button ---
WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "modalButton0")))
driver.find_element(By.ID, "modalButton0").click()

print("[+] Restore initiated. Please wait for STAT ligth to turn Green.")
time.sleep(50) # takes about 50s typicly. closing early hasnt broke it yet, though could be missleading. 
driver.quit()
