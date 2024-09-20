class Packet:
    def __init__(self, src, dst, payload, protocol="TCP"):
        # パケットの送信元、宛先、ペイロード、プロトコルの初期化
        self.src = src
        self.dst = dst
        self.payload = payload
        self.protocol = protocol

    def get_info(self):
        # パケットの基本情報を文字列で返す
        return f"Packet from {self.src} to {self.dst}, protocol: {self.protocol}, payload: {self.payload}"