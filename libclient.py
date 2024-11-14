
import sys
import selectors
import json
import io
import struct
import time


class Message:
    def __init__(self, selector, sock, addr, request):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self.request = request
        self._recv_buffer = b""
        self._send_buffer = b""

    def _set_selector_events_mask(self, mode):
        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {repr(mode)}.")
        self.selector.modify(self.sock, events, data=self)

    def _read(self):
        try:
            self._recv_buffer = self.sock.recv(4096)
        except BlockingIOError:
            pass

    def _write(self):
        
        if self.request["content"]["action"] == "start" or self.request["content"]["action"] == "Start":
            self._send_buffer = self._json_encode(self.request, self.request["encoding"])

        # Handles input based on situation

        elif self.request["content"]["action"] == "Welcome":
            action = "Option"
            value = input("username: ")
            message = dict(type="text/json", encoding="utf-8", content=dict(action=action, value=value),)
            message = self._json_encode(message, message["encoding"])
            self._send_buffer = message            

        elif self.request["content"]["action"] == "Question":
            action = "Answer"
            value = input("Answer: ")
            message = dict(type="text/json", encoding="utf-8", content=dict(action=action, value=value),)
            message = self._json_encode(message, message["encoding"])
            self._send_buffer = message

        elif self.request["content"]["action"] == "Correct":
            message = dict(type="text/json", encoding="utf-8", content=dict(action="Complete", value="Complete"),)
            message = self._json_encode(message, message["encoding"])
            self._send_buffer = message

        elif self.request["content"]["action"] == "Waiting":
            username = self.request["content"]["value"]
            message = dict(type="text/json", encoding="utf-8", content=dict(action="Option", value=username),)
            message = self._json_encode(message, message["encoding"])
            self._send_buffer = message  

        elif self.request["content"]["action"] == "Notified":
            username = self.request["content"]["value"]
            message = dict(type="text/json", encoding="utf-8", content=dict(action="Option", value=username),)
            message = self._json_encode(message, message["encoding"])
            self._send_buffer = message 

        elif self.request["content"]["action"] == "Winner":
            message = dict(type="text/json", encoding="utf-8", content=dict(action="Finished_Waiting", value="None"),)
            message = self._json_encode(message, message["encoding"])
            self._send_buffer = message 

        elif self.request["content"]["action"] == "Winner_Waiting":
            message = dict(type="text/json", encoding="utf-8", content=dict(action="Finished_Waiting", value="None"),)
            message = self._json_encode(message, message["encoding"])
            self._send_buffer = message           

        elif self.request["content"]["action"] == "Won" or self.request["content"]["action"] == "Loss":
            message = dict(type="text/json", encoding="utf-8", content=dict(action="Finished", value="None"),)
            message = self._json_encode(message, message["encoding"])
            self._send_buffer = message    

        elif self.request["content"]["action"] == "Reset":
            action = "Reset"
            value = input("Response: ")
            message = dict(type="text/json", encoding="utf-8", content=dict(action=action, value=value),)
            message = self._json_encode(message, message["encoding"])
            self._send_buffer = message 

        elif self.request["content"]["action"] == "Username":
            action = "Option"
            value = input("username: ")
            message = dict(type="text/json", encoding="utf-8", content=dict(action=action, value=value),)
            message = self._json_encode(message, message["encoding"])
            self._send_buffer = message   
        
        self.sock.send(self._send_buffer)
        self._send_buffer = b""


    def _json_encode(self, obj, encoding):
        return json.dumps(obj, ensure_ascii=False).encode(encoding)

    def _json_decode(self, json_bytes, encoding):
        tiow = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=""
        )
        obj = json.load(tiow)
        tiow.close()
        return obj

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()

    def read(self):
        
        self._read()
        message = self._json_decode(self._recv_buffer,"utf-8")
        self.request = message
    
        if(message["content"]["action"] == "Notified"):
            pass
        elif(message["content"]["action"] == "Winner_Waiting"):
            pass
        elif(message["content"]["action"] == "Waiting"):
            print("")
            print("Waiting for second player.")
        else:
            print("")
            print(message["content"]["value"])
        self._set_selector_events_mask("w")

    def write(self):

        self._write()

        self._set_selector_events_mask("r")

    def close(self):
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            pass

        try:
            self.sock.close()
        except OSError as e:
            pass
        finally:
            self.sock = None

