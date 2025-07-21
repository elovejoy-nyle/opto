#!/usr/bin/env python3
from scapy.all import sniff, Ether, get_if_hwaddr
'''
Notes: 
We are assuimg that the network structure is something like  the PC and the OPTO direct connection.
We are also assuming the device is an opto. realisticly, this code will find any other 
attached device mac address and assume it is an opto. 
We're also assuming our interface name as Ethernet4, rather than trying to define it using any OS 
specific determinations. will fix that later. 
'''
# Format the peer MAC address to the OPTO hostname format
def format_opto(mac_str):
    parts = mac_str.lower().split(":")[-3:]
    return f"https://opto-{parts[0]}-{parts[1]}-{parts[2]}"

def find_peer_mac(interface):
    my_mac = get_if_hwaddr(interface).lower()
    print(f"My MAC on {interface}: {my_mac}")

    found = {"mac": None}

    def handle(pkt):
        if Ether in pkt:
            src = pkt[Ether].src.lower()
            if src != my_mac:
                found["mac"] = src  # store the MAC to print later
        return

    def should_stop(pkt):
        return Ether in pkt and pkt[Ether].src.lower() != my_mac

    print("Searching for peer (OPTO) device")
    sniff(iface=interface, prn=handle, stop_filter=should_stop, timeout=10)

    if found["mac"]:
        print(f"Peer MAC address: {found['mac']}")
        print(f"Opto hostname:\n{format_opto(found['mac'])}")
    else:
        print("No device found.")

find_peer_mac("Ethernet 4")
