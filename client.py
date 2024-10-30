import sys
import socket
import selectors
import types
import random

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

def create_request(action, value):
    if action == "start" or action == "Start":
        return dict(
            type="text/json",
            encoding="utf-8",
            content=dict(action=action, value=value),
        )
    else:
        return dict(
            type="text/json",
            encoding="utf-8",
            content=dict(action=action, value=value),
        )

host, port = sys.argv[1], int(sys.argv[2])
action, value = sys.argv[3], sys.argv[4]
request = create_request(action, value)

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
finally:
    sel.close()