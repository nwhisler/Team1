import sys
import socket
import selectors
import types
import errno 

sel = selectors.DefaultSelector()

questions = {"Question 1": "Answer 1","Question 2": "Answer 2","Question 3": "Answer 3","Question 4": "Answer 4"}

def accept_wrapper(sock):
    conn, addr = sock.accept()
    conn.setblocking(False)
    conn.send("To start game type start".encode())
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"", correct=0, questions=[], previousQuestion = "", sentStart=True)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data: 
            if(recv_data.decode() == "Incorrect start to game. Type start to start game."):
                data.outb += recv_data    
            elif(recv_data.decode() == "Nothing sent."):
                data.outb += "No answer provided. Game terminating.".encode() 
            elif len(data.previousQuestion) > 0:
                answer = recv_data.decode()
                if answer == questions[data.previousQuestion]:
                    data.correct += 1
                data.outb = recv_data 
            elif(recv_data.decode() == "Start" or recv_data.decode() == "start"):
                    data.outb += recv_data    
        else:
            if(len(data.questions) == len(questions.keys())):
                sel.unregister(sock)
                sock.close()
            
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            if data.outb.decode() == "Incorrect start to game. Type start to start game.":
                sock.send(data.outb)
                data.outb = b""
                sel.unregister(sock)
                sock.close()  
            elif data.outb.decode() == "No answer provided. Game terminating.":
                sock.send(data.outb)
                data.outb = b""
                sel.unregister(sock)
                sock.close()                 
            elif(len(data.questions)) != len(questions.keys()):
                for questionKey in questions.keys():
                    if questionKey not in data.questions:
                        sock.send(questionKey.encode())
                        data.previousQuestion = questionKey
                        data.questions.append(questionKey)
                        data.outb = b""
                        break
            else:
                sock.send(("Quiz completed number of correct " + str(data.correct)).encode())
                sel.unregister(sock)
                sock.close()

host, port = sys.argv[1], int(sys.argv[2])

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)
sockets = set()

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:            
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()