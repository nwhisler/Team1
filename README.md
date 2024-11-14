# Team1

# Quiz

This is a simple quiz game implemented using Python and sockets.

**How to play:**
1. **Start the server:** Run the `server.py` script with python3 server.py -p port_number.
2. **Connect clients:** Run the `client.py` script on two different machines or terminals with python3 client.py -i ip_address -p port_number
3. **Play the game:** Players take turns entering their answers. The player with the most correct answers wins.
4. **To Leave:** Enter either Leave or leave during username or answer input.

**Message Protocol Schema**
* {type="text/json", encoding="utf-8", content= {action="action", value="value}}

**Explicit actions:**
* Start or start, starts the quiz game.

**Implicit actions:**
* Waiting, waiting for a second player
* Notified, player has been notified of waiting period
* Question, question has been asked
* Answer, answer has been given.

**Technologies used:**
* Python
* Sockets

**Additional resources:**
* https://www.python.org/
* https://docs.python.org/3/library/socket.html
