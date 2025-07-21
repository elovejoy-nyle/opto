from scapy.all import sniff, Ether, get_if_hwaddr
import subprocess



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
    #return f"opto-{parts[0]}-{parts[1]}-{parts[2]}"

# Example usage
interface_name = "Ethernet 4"  # Update as needed
rio_mac = get_peer_mac(interface_name)

if rio_mac:
    print(f"Connected peer MAC: {rio_mac}")

    last_3_bytes = ":".join(rio_mac.split(":")[-3:])
    print(f"Last 3 bytes: {last_3_bytes}")

    formatted = format_opto(rio_mac)
    print(f"Formatted name: {formatted}")
    post_url = f"{formatted}/commissioning/start.html"

    first_login = [
        "curl", "-k", "-L", "-X", "POST", post_url,
        "-d", "uname=nyle",
        "-d", "pwd=nyle1234",
        "-d", "confirmPwd=nyle1234"
    ]
    result = subprocess.run(first_login, capture_output=True, text=True)
    print("Status:", result.returncode)
    print("Output:", result.stdout)
    #login_CMD = ["curl", formatted, "-d \"uname=nwhs\"", "-d \"pwd=Fullservice1!\"" ]
    
    
else:
    print("No peer MAC detected.")

''' to use cURL:
-d offers a data frame the same way as a browser via POST
so then yo need the identifyer for that data,. which means you look at the source code 
for the web page, and read the fields where the data you are trying to sen goes.
          <label for="uname">Username</label>
          <input id="uname" name="uname" type="text" class="form-control">
        
          <label for="pwd">Password</label>
          <input id="pwd" name="pwd" type="password" class="form-control" onkeypress="checkEnterSubmit(event)">

So here, username and password are named uname and pwd

Our cURL request will then look like this:
curl http://opto-last_3_bytes -d "uname=nwhs" -d "pwd=somepassword"

on the first loggin the request will need to be set up,
so the format will be:
 curl http://opto-last_3_bytes -d "uname=nyle" -d "pwd=nyle1234" -d "confirmed=nyle1234"
 {{{{{{ probably ... or something very similar to that }}}}}} 
 the uncertenty here is if the repeat password field holds the same filed id as the first one.
 for that I would need to reset the OPTO.. but im holding off on that for a minute
 
'''
################ INTI PROCESS ########################

''' STEP 1: click the lets get started button links to :https://opto-05-33-c7/commissioning/start.html
    <div class="jumbotron">
      <h1 class="welcome-title">Welcome!</h1>
      <img src="/auth-static/images/groovRIO_576x204.png" class="logo">
      <a href="/commissioning/start.html" class="btn btn-primary btn-lg">
        Let's get started!&nbsp;<i class="fa fa-arrow-circle-right"></i>
      </a>


## we can skip this page though, as it is just a link to 
https://{formatted}/commissioning/start.html
http://{formatted}/commissioning/start.html

###### First login form: 
        <form id="form" action="/auth/access/user/commission/form" method="post" enctype="application/x-www-form-urlencoded" onsubmit="return validateInput()">
          <input type="hidden" name="csrf" value="wyhYGujph7xj5XiJKQ6QNDfGy2yAt9Xh">
          <div id="uname-container" class="form-group">
            <label class="control-label" for="uname">Username</label>
            <input id="uname" name="uname" type="text" class="form-control">
            <div class="input-err-msg">Username must be between 1 and 128 characters in length.</div>
          </div>
          <div id="pwd-container" class="form-group">
            <label class="control-label" for="pwd">Password</label>
            <input id="pwd" name="pwd" type="password" class="form-control">
            <div class="input-err-msg">Password must be between 1 and 128 characters in length.</div>
          </div>
          <div id="pwd-confirm-container" class="form-group">
            <label class="control-label" for="confirmPwd">Confirm Password</label>
            <input id="confirmPwd" name="confirmPwd" type="password" class="form-control" onkeypress="checkEnterSubmit(event)">
            <div class="input-err-msg">Must match <em>Password</em> above.</div>
          </div>
          <div class="align-right signin-btns">
            <button id="submitBtn" type="submit" class="btn btn-primary"><i class="fa fa-sign-in"></i>&nbsp;Create Account</button>
          </div>
        </form>





'''
















































