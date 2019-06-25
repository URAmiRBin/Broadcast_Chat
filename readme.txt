Run Tkinker.py for both client and server
I used Tkinter to implement GUI
Main Network code is in server.py
This is an anynomous chat, so there's only two people to chat with each other
This Chat application censors curse words`
PROTOCOL:
1. Run Broadcaster FIRST
2. Broadcaster Broadcasts for 4 seconds then listens for 5 seconds
3. If no one answered broadcaster closes itself
4. Listener Listens for 5 seconds
5. If no one broadcasts "hello" listener closes itself
6. So at least we have 4 seconds between to start broadcaster and listener
7. This time can be changed in code
8. I used ports 2222, 3333, 4444 for doing broadcast and listen
9. Type [!q] to finish chat or close chat windows
