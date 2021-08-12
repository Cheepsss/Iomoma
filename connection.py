import time
import socket
import json
from collections import deque
import threading
import sys
import time


class Connection():
    def __init__(self):
        self.msgFromClient = "f"
        self.bytesToSend         = str.encode(self.msgFromClient)
        self.serverAddressPort   = ("185.185.127.92", 10001)
        self.bufferSize          = 10000
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)
        self.sock.sendto(self.bytesToSend, self.serverAddressPort)
        self.sock.settimeout(30)
        self.found_player = True
        self.q_end = deque()
        self.q_listen = deque()
        self.q_send = deque()
        try:
            self.msgFromServer = self.sock.recvfrom(self.bufferSize)
        except socket.timeout:
            self.q_end.append("end")
            self.found_player = False
        if self.found_player:
            self.sock.settimeout(3)
            self.msg = self.msgFromServer[0]
            self.port = self.msg.decode("utf-8")
            self.port = int(self.port)
            self.serverAddressPort   = ("185.185.127.92", self.port)
            def listen(sock, buffer_size):
                while True:
                    try:
                        data_address = sock.recvfrom(buffer_size)
                    except socket.timeout:
                        self.q_end.append("end")
                        break
                    data = data_address[0].decode("utf-8")
                    data = json.loads(data)
                    self.q_listen.append(data)

            def send(sock,  serverAddressPort):
                while True:
                    if self.q_end:
                        break
                    if self.q_send:
                        data = self.q_send.popleft()
                        data = json.dumps(data)
                        data = bytes(data, 'utf-8')
                        sock.sendto(data, serverAddressPort)
                    else:
                        time.sleep(0.03)

            sock = self.sock
            buffer_size = self.bufferSize
            serverAddressPort = self.serverAddressPort
            self.thread = threading.Thread(target = listen, args = (sock, buffer_size,))
            self.thread2 = threading.Thread(target = send, args = (sock, serverAddressPort))
            self.thread.daemon = True
            self.thread2.daemon = True
            self.thread.start()
            self.thread2.start()
