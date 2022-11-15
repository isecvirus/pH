from tkinter import Listbox

import scapy.all as scapy

def get_login_info(packet, List:Listbox):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)

        for keyword in List.get(0, 'end'):
            if keyword in load:
                return load