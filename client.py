import sys
import socket
import selectors
import types
import random

sel = selectors.DefaultSelector()

def start_connections(host, port):

    connid = random.randrange(1, 50, 3)

    server_addr = (host, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    total_correct = 0
    data = types.SimpleNamespace(
        connid=connid,
        recv_total=0,
        message="",
        complete = "",
        outb=b"",
    )
    sel.register(sock, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.recv_total += len(recv_data)
            if recv_data.decode() == "To start game type start":
                print(recv_data.decode())
                data.message = input("Input: ")
                if(data.message != "Start" and data.message != "start"):
                    data.message = "Incorrect start to game. Type start to start game."
            elif "Quiz completed" in recv_data.decode():
                print(recv_data.decode())
                sel.unregister(sock)
                sock.close()
            elif recv_data.decode() == "No answer provided. Game terminating.":
                print(recv_data.decode())
                sel.unregister(sock)
                sock.close()   
            elif recv_data.decode() == "Incorrect start to game. Type start to start game.":
                print(recv_data.decode())
                sel.unregister(sock)
                sock.close()               
            else:
                print(recv_data.decode())
                data.message = input("Answer: ")
                if len(data.message) == 0:
                    data.message = "Nothing sent."
        if not recv_data:
            if data.complete == "Quiz completed":
                sel.unregister(sock)
                sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and len(data.message) > 0:
            data.outb = data.message.encode()
        if data.outb:
            sent = sock.send(data.outb)
            data.message = ""
            data.outb = b""


host, port = sys.argv[1], int(sys.argv[2])

start_connections(host, port)

try:
    while True:
        events = sel.select(timeout=1)
        if events:
            for key, mask in events:
                service_connection(key, mask)
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()