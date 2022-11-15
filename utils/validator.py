import re

class IP2NUM:
    def __init__(self, ip: str):
        self.ip = ip
        self.min_octet = 0
        self.max_octet = 0x100  # 256
        self.steps = 1

        # (ValueError) might happen if the ip is not completer 4 octets
        (self.i1, self.i2, self.i3, self.i4) = re.findall("(\d+)", self.ip)
        self.i1 = int(self.i1)
        self.i2 = int(self.i2)
        self.i3 = int(self.i3)
        self.i4 = int(self.i4)

    def get(self):
        o1 = ((self.max_octet * (self.max_octet * self.max_octet)) * self.i1)
        o2 = ((self.max_octet * self.max_octet) * self.i2)
        o3 = (self.max_octet * self.i3)
        o4 = self.i4
        return (o1 + o2 + o3 + o4)

class Validator:
    def protocol(self, proto):
        return proto in ["socks5", "socks", "http", "https"]
    def ip(self, ip:str):
        try:
            num = IP2NUM(ip).get()
            if num >= 0 and num <= 4294967295: # 4294967295 is the maximum ip range (255.255.255.255)
                return True
            else:
                return False
        except Exception:
            return False
    def port(self, port:int or str):
        try:
            return int(port) >= 0 and int(port) <= 65535
        except Exception:
            return False
    def timeout(self, second:float):
        try:
            return isinstance(float(second), float)
        except Exception:
            return False

validator = Validator()