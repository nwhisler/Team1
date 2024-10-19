# Team1

# Quiz

This is a simple quiz game implemented using Python and sockets.

**How to play:**
1. **Start the server:** Run the `server.py` script with python3 server.py ip_address port_number.
2. **Connect clients:** Run the `client.py` script on two different machines or terminals with python3 client.py ip_address port_number start None
3. **Play the game:** Players take turns entering their answers. The player with the most correct answers wins.

**Message Protocol**
Delivered through the libclient and libserver classes. Each consist of a Message class that contains the state of the game which it transfers from the client to the server and vice versa. The specific protocol structure used is JSON. The main message type is start which starts the game. It takes the action start with a value of none to begin the game. The classes libclient and libserver each have the same functions to encode and decode the JSON message structure. They decode upon recieval and then encode upon construction of a reply and then send the message. 

**Technologies used:**
* Python
* Sockets

**Additional resources:**
* https://www.python.org/
* https://docs.python.org/3/library/socket.html
