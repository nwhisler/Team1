
import sys
import selectors
import json
import io
import struct

questions = {"Question 1": "Answer 1","Question 2": "Answer 2","Question 3": "Answer 3","Question 4": "Answer 4"}

class Message:
    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self.request = None
        self._recv_buffer = b""
        self._send_buffer = b""
        self.previousQuestion = None
        self.correct = 0
        self.closed = False

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
            message = dict(type="text/json", encoding="utf-8", content=dict(action="Question", value="Question 1"),)
            message = self._json_encode(message, message["encoding"])
            self._send_buffer += message
            self.previousQuestion = "Question 1"
        elif self.previousQuestion:
            if self.previousQuestion == "Question 1":
                message = dict(type="text/json", encoding="utf-8", content=dict(action="Question", value="Question 2"),)
                message = self._json_encode(message, message["encoding"])
                self._send_buffer += message
                self.previousQuestion = "Question 2"
            elif self.previousQuestion == "Question 2":
                message = dict(type="text/json", encoding="utf-8", content=dict(action="Question", value="Question 3"),)
                message = self._json_encode(message, message["encoding"])
                self._send_buffer += message
                self.previousQuestion = "Question 3"
            elif self.previousQuestion == "Question 3":
                message = dict(type="text/json", encoding="utf-8", content=dict(action="Question", value="Question 4"),)
                message = self._json_encode(message, message["encoding"])
                self._send_buffer += message
                self.previousQuestion = "Question 4"
            elif self.previousQuestion == "Question 4":
                message = dict(type="text/json", encoding="utf-8", content=dict(action="Correct", value="Total correct " + str(self.correct)),)
                message = self._json_encode(message, message["encoding"])
                self._send_buffer += message
                self.previousQuestion = "Done"
            elif self.previousQuestion == "Done":
                self.closed = True
                self.close()

        if not self.closed:
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

        if self._recv_buffer:

            message = self._json_decode(self._recv_buffer,"utf-8")
            self.request = message
            if message["content"]["action"] == "Answer":
                if self.previousQuestion == "Question 1":
                    if message["content"]["value"] == questions[self.previousQuestion]:
                        self.correct += 1
                elif self.previousQuestion == "Question 2":
                    if message["content"]["value"] == questions[self.previousQuestion]:
                        self.correct += 1
                elif self.previousQuestion == "Question 3":
                    if message["content"]["value"] == questions[self.previousQuestion]:
                        self.correct += 1
                elif self.previousQuestion == "Question 4":
                    if message["content"]["value"] == questions[self.previousQuestion]:
                        self.correct += 1

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
        except Exception:
            pass
        finally:
            self.sock = None

