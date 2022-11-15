import scapy.layers.http

def get_url(packet):
    host = packet[scapy.layers.http.HTTPRequest].Host
    path = packet[scapy.layers.http.HTTPRequest].Path
    return host + path
