import subprocess
from controller.getMac import get_mac
import scapy.all as scapy
from utils.debug import dbg, INFO, ERROR, SUCCESS

"""
SEE: https://stackunderflow.dev/p/iptables-for-routing
Jump(NFQUEUE, MASQUERADE, SNAT, DNAT)


# modprobe iptable_nat
# iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
# iptables -A FORWARD -i eth1 -j ACCEPT

echo 1 > /proc/sys/net/ipv4/ip_forward
sudo iptables -I FORWARD -j NFQUEUE --queue-num 0
-I  insert
-i  interface
-t  tables
-A  append to chain
-o  output interface
-j  jump [TARGET]
"""

_input_ = "INPUT"
_output_ = "OUTPUT"
_forward_ = "FORWARD"
_jump_ = "NFQUEUE"
queue = 0

forward_locally = [
    f"sudo iptables -I {_input_} -j {_jump_} --queue-num {str(queue)}",
    f"sudo iptables -I {_output_} -j {_jump_} --queue-num {str(queue)}",
    # f"sudo echo 1 > /proc/sys/net/ipv4/ip_forward"
]
forward_remotely = [
    f"sudo iptables -I {_forward_} -j {_jump_} --queue-num {str(queue)}",
    "sudo echo 1 > /proc/sys/net/ipv4/ip_forward"
]
unForward = [
    "sudo iptables --flush",
    "sudo echo 0 > /proc/sys/net/ipv4/ip_forward"
]

# Send an ARP response with the real values (stop spoofing)
def reset(dest_ip, src_ip):
    try:
        destination_mac = get_mac(dest_ip)
        src_mac = get_mac(src_ip)
        packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=destination_mac, psrc=src_ip, hwsrc=src_mac)
        scapy.send(packet, count=4, verbose=False)
    except Exception:
        pass


def Route_Locally():
    dbg("Forwarding packets locally..", INFO)
    for fl in forward_locally:
        subprocess.Popen(fl, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

def Route_Remotely():
    dbg("Forwarding packets remotely..", INFO)
    for fr in forward_remotely:
        subprocess.Popen(fr, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

def Flush():
    dbg("Flushing tables..", INFO)
    for uf in unForward:
        subprocess.Popen(uf, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
