# CLUBROOM 


### Description
Clubroom is a web-based chatting app that lets users create and join chat rooms for real-time communication. Whether you're chatting with friends, working with a team, or just hanging out, Clubroom makes staying connected easy and fun.

### Features
- User Authentication: This ensures the app is secure, protecting user data and privacy. The registration system uses modern hashing techniques to securely store passwords.

- Unlimited Rooms: There’s no limit to the number of rooms that can be created, enabling flexibility for users. Each room is uniquely identifiable by its name.

- Real-time Communication: Leveraging WebSockets, users can send and receive messages instantly. For instance, messages appear immediately without requiring a page refresh.
  
- Message History: Rooms and their messages are stored in a database, making it easy to revisit conversations later. For example, teams working on a project can track their discussions.

- Automatic Cleanup: To save storage, unused rooms and associated messages are automatically deleted when everyone leaves the room.

### Tools Used

- HTML and CSS: Used to design and structure the user interface, ensuring a visually appealing and user-friendly experience.

- Flask Framework: Powers the backend of the application, enabling smooth handling of user requests, database interactions, and server-side logic.

- Flask-SocketIO: Enables real-time, bi-directional communication between the client and server, ensuring messages are instantly delivered to all participants in a room.

- SqlAlchemy: Manages the database, storing user information, room details, and message history securely and efficiently.

- WebSockets: Facilitates real-time data exchange, allowing users to chat seamlessly without refreshing the page.

### Project Files 
**1. templates (Folder)**

The templates folder is where all the HTML files for the app reside. Flask uses this directory to render pages dynamically with data passed from the backend.

**2. .gitignore (File)**

This is a text file that specifies which files or folders Git should ignore when committing changes. For example, environment files, session data, or log files.

**3. app (Python Source File)**

This file likely serves as the main entry point for the Flask application. It contains the routes, views, and logic for handling user requests and rendering responses.

**4. README (Markdown Source File)**

This is a markdown file that typically provides an overview of the project. It includes the app's description, installation steps, usage instructions.

**5. requirements (Text Document)**

This is a requirements.txt, which lists all the Python dependencies needed for the app to work. It helps users easily set up the project by running pip install -r requirements.txt.

### Step-by-step Guide

**1. User Registration and Login**

- When you open Clubroom, the first page you’ll see is the user authentication page.
- If you're a new user, click on the "Register" button and create an account by providing a unique username and a strong password (a mix of letters, numbers, and symbols).
- If you already have an account, simply log in using your credentials to access the app.

**2. Dashboard Overview**

 - After logging in, you’ll be directed to the main dashboard. Here, you’ll find options to create a new room or join an existing room.
- The dashboard displays a clean interface, making it easy to navigate between options.


**3. Create a Room**

- To create a new room, click on the "Create Room" button.
- Enter a unique room name in the provided field. Once created, you’ll be redirected to the chat room where you can start messaging.
- You can share the room name with friends so they can join and chat with you.

**4. Join a Room**

- If you’ve been invited to an existing room, click on the "Join Room" button.
- Enter the name of the room you want to join. If the name matches an active room, you’ll be added to it instantly.
- Once inside, you can participate in the conversation with other members.

**5. Real-time Messaging**

- Once in a chat room, type your messages in the input box and hit "Send."
- Your messages will appear instantly for all participants in real-time, thanks to the app’s WebSocket functionality.
- You can see the history of messages in the chat room, making it easy to follow the conversation.

**6. Room and Message Management**

- Clubroom stores room information and message history in its database while the chat room is active.
- If you need to leave temporarily, the room will remain active as long as at least one person stays in it.

**7. Automatic Deletion**

- Once all participants leave a room, the room and all its associated messages are automatically deleted from the database.
- This feature ensures privacy and keeps the system clean by removing unused rooms.

**8. Logout**

- When you’re done, click on the "Logout" button to safely exit your account.
