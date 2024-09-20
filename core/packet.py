class Packet:
    def __init__(self, src, dst, payload, protocol="TCP"):
        self.src = src
        self.dst = dst
        self.payload = payload
        self.protocol = protocol

    def get_info(self):
        return f"Packet from {self.src} to {self.dst}, protocol: {self.protocol}, payload: {self.payload}"