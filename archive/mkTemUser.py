import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from scapy.all import sniff, Ether, get_if_hwaddr


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
    return f"https://opto-{parts[0]}-{parts[1]}-{parts[2]}"

def create_opto_user(hostname, username, password):
    base_url = f"https://{hostname}"
    session = requests.Session()

    # Step 1: Load the commissioning form to get CSRF token
    page = session.get(f"{base_url}/commissioning/start.html", verify=False)
    soup = BeautifulSoup(page.text, "html.parser")

    # Extract CSRF token
    csrf = soup.find("input", {"name": "csrf"})
    if not csrf:
        print("CSRF token not found.")
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
        print("Account created successfully.")
        return True
    else:
        print("Account creation failed.")
        print("Status code:", resp.status_code)
        print("Response:", resp.text[:1000])  # Preview response
        return False

# === Main Logic ===
interface_name = "Ethernet 4"  # Adjust to match your environment

rio_mac = get_peer_mac(interface_name)

if rio_mac:
    formatted = format_opto(rio_mac)
    hostname = formatted.replace("https://", "")
    print(f"Formatted hostname: \nhttps://{hostname}")
    create_opto_user(hostname, "nyle", "nyle1234")
else:
    print("No peer MAC address detected.")
