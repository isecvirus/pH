import scapy.all as scapy


def get_mac(ip, timeout:int=1) -> str:
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=timeout, verbose=False)[0]

    """
    QueryAnswer(
        query=<
            Ether  dst=ff:ff:ff:ff:ff:ff type=ARP |<
                ARP  pdst=192.168.100.183 |
            >
        >,
        answer=<
            Ether  dst=e4:54:e8:d4:d6:6c src=00:c0:ca:ae:54:98 type=ARP |<
                ARP  hwtype=0x1 ptype=IPv4 hwlen=6 plen=4 op=is-at hwsrc=00:c0:ca:ae:54:98 psrc=192.168.100.183 hwdst=e4:54:e8:d4:d6:6c pdst=192.168.100.2 |
                <
                    Padding  load='\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' |
                >
            >
        >
    )
    """
    return str(answered_list[0][1].hwsrc)
