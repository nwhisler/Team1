import sys
import socket
import selectors
import types
import errno 

import libserver

# Selector handles questions for each player so that each player takes the same quiz.

sel = selectors.DefaultSelector()

questions = {"Question 1": "Answer 1","Question 2": "Answer 2","Question 3": "Answer 3","Question 4": "Answer 4"}

number_of_players = 0
previous_player_completion = False

def accept_wrapper(sock):
    conn, addr = sock.accept()
    conn.setblocking(False)
    message = libserver.Message(sel, conn, addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=message)

host, port = sys.argv[1], int(sys.argv[2])

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:            
            if key.data is None:
                number_of_players += 1
                accept_wrapper(key.fileobj)
            else:
                message = key.data
                try:
                    message.process_events(mask, number_of_players)
                except Exception:
                    number_of_players -= 1
                    message.close()
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()