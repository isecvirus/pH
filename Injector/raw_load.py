from scapy.layers.inet import IP, TCP
from scapy.packet import Raw, Packet


def manipulate(packet: Packet, load):  # manipulate load
    """
    :param packet: scapy packet
    :param load: new html code to set as a new raw load
    :return:
    """
    packet[Raw].load = load
    del packet[IP].len
    del packet[IP].chksum
    del packet[TCP].chksum
    return packet
