import sys
import socket
import selectors
import types
import random
import argparse

import libclient

sel = selectors.DefaultSelector()

def start_connections(host, port, request):

    connid = random.randrange(1, 50, 3)

    server_addr = (host, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    total_correct = 0
    message = libclient.Message(sel, sock, server_addr, request)
    sel.register(sock, events, data=message)

def create_request():
    
        return dict(
            type="text/json",
            encoding="utf-8",
            content=dict(action="start", value="value"),
        )

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--ip')
parser.add_argument('-p', '--port')

args = parser.parse_args()

host, port = args.ip, int(args.port)
request = create_request()

start_connections(host, port, request)

try:
    while True:
        events = sel.select(timeout=1)
        if events:
            for key, mask in events:
                message = key.data
                try:
                    message.process_events(mask)
                except Exception:
                    message.close()
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
    print("Reset Server.")
finally:
    sel.close()