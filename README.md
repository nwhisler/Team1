# Team1

# Quiz

This is a simple quiz game implemented using Python and sockets.

**How to play:**
1. **Start the server:** Run the `server.py` script with python3 server.py -p port_number.
2. **Connect clients:** Run the `client.py` script on two different machines or terminals with python3 client.py -i ip_address -p port_number
3. **Play the game:** Players take turns entering their answers. The player with the most correct answers wins.
4. **To Leave:** Enter either Leave or leave during username or answer input.
5. **Current Questions and Answers:** {"What is 2 * (5 + 5 / 5)?": "C","What is the capital of the US?": "A","Where is the Eiffel Tower?": "D","How many states are there?": "B"}

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

**Security Concerns:**
* Buffer overflow attacks pose a significant risk as they can overwrite adjacent memory sections, potentially allowing attackers to gain control over a system or access sensitive information. This concern can be mitigated by restricting the buffer to a specified size, carefully reading only the intended amount of data, using the retrieved value for string comparison, and resetting the buffer afterward. Injection attacks, which manipulate the program into executing unintended actions, are less of a concern here due to the absence of accessible SQL or command line interfaces that could be exploited for such attacks.

**Roadmap:**
* I would enhance the project by transforming it into a more dynamic experience, where questions are selected and presented randomly, and the question pool is expanded beyond just four. Additionally, I would improve the user interface by incorporating more graphics and making it more interactive for a richer user experience.

**Retrospective:**
* The key success of the project was the development and implementation of its core functionality. The game meets all the specified requirements effectively and operates as intended. Additionally, it has minimal security concerns.
* An area for improvement would be a more spacious and user-friendly interface layout, avoiding the current cramped design, as well as an expansion of the question pool.

**Additional resources:**
* https://www.python.org/
* https://docs.python.org/3/library/socket.html
