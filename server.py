import socket
import multiprocess


#serverul e pe localhost, serverul meu functioneaza pe ip-ul din connection.py

def new_lobby(port, addr1, addr2):
    import socket
    from collections import deque
    import threading
    import time
    import queue

    address1 = addr1
    address2 = addr2
    local_ip = "127.0.0.1"
    local_port = port
    buffer_size = 1024
    print(port)
    sock = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
    sock.bind((local_ip, local_port))
    sock.settimeout(5)
    running  = True
    q = deque()
    closing_queue= queue.Queue(1)
 
    def listen(sock, running):
        buffer_size = 1024
        while running:
            try:
                data_address = sock.recvfrom(buffer_size)
                q.append(data_address)
            except socket.timeout:
                closing_queue.put(False)
    def send(sock, address1, address2):
        while True:
            if q:
                data_address = q[0]
                q.popleft()
                if data_address:
                    if data_address[1] == address1:
                        sock.sendto(data_address[0], address2)
                    else:
                        sock.sendto(data_address[0], address1)
            else:
                time.sleep(0.01)
    thread1 = threading.Thread(target = listen, args=(sock, running, ), daemon = True)
    thread2 = threading.Thread(target = send, args = (sock, address1, address2), daemon = True)
    thread1.start()
    thread2.start()
    while running:
        time.sleep(5)
        if closing_queue.qsize() > 0:
            running = False
    print("process_closing")


 
 
local_ip = "127.0.0.1"
local_port = 10001
buffer_size = 1024
 
server_message = "connected"
byte_server_message = str.encode(server_message)
sock = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
sock.bind((local_ip, local_port))
lobby = []
port_count = 10002
check_alive = False
 
while True:
    message, address = sock.recvfrom(buffer_size)
    message = message.decode("utf-8")
    print(address, " ", message)
    if address not in lobby:
        lobby.append(address)
    if len(lobby) == 2:
        p = multiprocess.Process(target = new_lobby, args = (port_count,lobby[0], lobby[1]))
        p.start()
        port = str(port_count)
        port = port.encode()
        for address in lobby:
            print(address)
            sock.sendto(port,address)
        port_count += 1
        lobby = []
        check_alive = True

