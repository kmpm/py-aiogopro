import asyncio
import time

HEARTBEAT_TIMEOUT = 2

class KeepAliveProtocol(asyncio.DatagramProtocol):
    def __init__(self, loop):
        self.loop = loop
        self._continue = True

    def connection_made(self, transport):
        print('connection_made')
        self.transport = transport
        self.keepalive()

    def error_received(self, exc):
        print('Error received:', exc, dir(exc))
        # self.quit()

    def connection_lost(self, exc):
        print("Connection closed")
        self.on_con_lost.set_result(True)
        self.quit()

    def quit(self):
        self._continue = False
        print('ka quit')

    def keepalive(self):
        print('keepalive called')
        self.transport.sendto("_GPHD_:0:0:2:0.000000\n".encode())
        if self._continue:
            self.h_timeout = asyncio.get_event_loop().call_later(HEARTBEAT_TIMEOUT, self.keepalive)


#  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.sendto("_GPHD_:0:0:2:0.000000\n".encode(), (self.ip_addr, 8554))
# time.sleep(2500 / 1000)
