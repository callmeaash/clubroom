# CLUBROOM 


### Description
Clubroom is a web chatting app where user can create rooms and chat with each other in real time.

### Features
- User authenticaton option for security

- Create as much rooms as you want

- Multiple people can join the room

- Real time communication with friends
  
- The rooms and the messages records are stored in the database which provides the history

- Once Everyone leaves the room, the room and the messages records are automatically deleted

### Tools Used

- HTML and CSS for frontend

- Flask framework for the backend

- Flask-SocketIO for realtime bi-directional communication betweens client and server

- SqlAlchemy for the database to store users info, rooms info and messages history 

### Step-by-step Guide

**1. User Authentication:** 
- As the web app opens the first page is the user authentication page. If you are a new user, first register yourself. the username should be unique and the password must be strong i.e. combination of character, symbols and numbers.

**2. Join Room:** 
- If you have a room name already just click on 'Join room' and enter the chat

**3. Create Room:**
- Create a room (room name must be unique) if you dont already have the chatroom created.

**4. Create Room:**
- Once the chatting is completed everyone leave the chatroom and that room is automatically deleted along with all the messages associated with that room
