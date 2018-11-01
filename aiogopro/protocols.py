import asyncio


class KeepaliveProtocol(asyncio.DatagramProtocol):
    def __init__(self, loop):
        self.loop = loop

    def connection_made(self, transport):
        self.transport = transport
        self.keepalive()

    def keepalive(self):
        self.transport.sendto("_GPHD_:0:0:2:0.000000\n".encode())


#  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.sendto("_GPHD_:0:0:2:0.000000\n".encode(), (self.ip_addr, 8554))
# time.sleep(2500 / 1000)
