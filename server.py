import sys
import socket
import selectors
import types
import errno 
import argparse

import libserver

sel = selectors.DefaultSelector()

# Stores scores and whether a quiz has been completed.

scores = {}
completed = {}
reset = 0

questions = {"Question 1": "Answer 1","Question 2": "Answer 2","Question 3": "Answer 3","Question 4": "Answer 4"}

number_of_players = 0
previous_player_completion = False

def accept_wrapper(sock):
    conn, addr = sock.accept()
    conn.setblocking(False)
    message = libserver.Message(sel, conn, addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=message)

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port')

args = parser.parse_args()

host, port = "0.0.0.0", int(args.port)

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

                    # Stores relevant information for both player's quiz.

                    message.process_events(mask, number_of_players)
                    score = message.score()
                    address = message.address()
                    scores[address] = score
                    complete = message.get_completed()
                    completed[address] = complete
                    values = list(set(completed.values()))
                    if len(values) == 1 and values[0] == True:
                        for key in scores.keys():
                            if key != address:
                                message.set_opponent_score(scores[key])
                                # Winning conditions
                                if scores[key] > score:
                                    message.declare_winner(False)
                                else:
                                    message.declare_winner(True)
                        if message.get_reset_answered():
                            reset += 1
                    if reset == 2:
                        scores = {}
                        completed = {}
                        reset = 0
                except Exception:
                    number_of_players -= 1
                    message.close()
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()