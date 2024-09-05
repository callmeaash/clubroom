from flask import Flask, redirect, session, render_template, flash, request, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import re
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_socketio import join_room, leave_room, send, SocketIO
from datetime import datetime
# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

socketio = SocketIO(app)
# Configure database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clubroom.db'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash = db.Column(db.String(120), nullable=False)
    messages = db.relationship('Messages', backref='room', lazy=True)

class Rooms(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    members = db.Column(db.Integer, default=0)
    messages = db.relationship('Messages', backref='user', lazy=True)

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message_text = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)

# Function for login require decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

# Prevent Caching
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Login route
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Check if username was submitted
        if not username:
            return render_template("login.html", username_error="Enter Username", password_error=None)
        
        # Check if password was submitted
        elif not password:
            return render_template("login.html", password_error="Enter Password", username_error=None, username=username)
        
        # Retrive record of user based on username
        user = Users.query.filter_by(username = username).first()

        # Check if the user exists
        if user is None:
           return render_template("login.html", username_error="Username not found")
        
        # Check if the password is correct
        elif not check_password_hash(user.hash, password):
           return render_template("login.html", password_error="Wrong Password")
        
        # Login the user 
        else:
           session["user_id"] = user.id
           session["username"] = user.username
           return redirect("/")
    else:
        return render_template("login.html")

# Main route / index route
@app.route('/', methods=["POST", "GET"])
@app.route('/index', methods=["POST", "GET"])
@login_required
def index():

    if request.method == "POST":
        
        # Redirect to /join route if user clicks on join room
        if "join" in request.form:
            return redirect('/join')
        
        # Redirect to /create route if user clicks on create room
        elif "create" in request.form:
            return redirect('/create')
        
    else:
        return render_template("index.html")

# Route to Join a room
@app.route('/join', methods=["POST", "GET"])
@login_required
def join():
    if request.method == 'POST':
        room_name = request.form.get("room")
        if not room_name:
            return render_template("join.html", error="Provide room name")

        room = Rooms.query.filter_by(name=room_name).first()

        if not room:
            return render_template("join.html", error="Room doesnot exist")
        else:
            session["room"] = room.name
            return redirect(url_for('room', room_id=room.id))
    else:
        return render_template("join.html")

# Route to Create a Room
@app.route('/create', methods=["POST", "GET"])
@login_required
def create():
    if request.method == 'POST':
        room = request.form.get("room")
        if not room:
            return render_template("create.html", error="Provide room name")
        
        try:
            new_room = Rooms(name=room)
            db.session.add(new_room)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return render_template("create.html", error="Room already exists")
        
        flash("Room created successfully")
        return redirect("/join")

    else:
        return render_template("create.html")

# Route for message room
@app.route("/room/<room_id>", methods=["GET", "POST"])
def room(room_id):
    if not 'room' in session:
        return redirect('/join')
    else:
        return render_template("room.html", name=session['room'])
    
@socketio.on("connect")
def connect():
    name = session['username']
    room = Rooms.query.filter_by(name=session['room']).first()
    if room:
        join_room(room.name)
        send({'name': name, 'message': 'has entered the room'}, to=room.name)
        room.members += 1
        db.session.commit()
        print(f"{name} joined the room")

@socketio.on("disconnect")
def disconnect():
    name = session['username']
    room = Rooms.query.filter_by(name=session['room']).first()
    if room:
        leave_room(room.name)
        send({'name': name, 'message': 'has left the room'}, to=room.name)
        room.members -= 1
        db.session.commit()
        if room.members <= 0:
            db.session.delete(room)
            db.session.commit()
        print(f"{name} joined the room")
        
# Route for register
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        # Check if username was submitted
        if not username:
            return render_template("register.html", username_error="Enter Username", password_error=None)
        
        # Check if password was submitted
        elif not password:
            return render_template("register.html", password_error="Enter Password", username_error=None, username=username)
        
        # Check if length of the password is at least 8 characters long
        elif len(password) < 8:
            return render_template("register.html", password_error="Password length must greater than 8", username=username)
        
        # Check if the password includes at least one character, number and a special character
        elif not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%#?&])[A-Za-z\d@$!%*#?&]{8,}$", password):
            return render_template("register.html", password_error="Must include atleast one character, number, special symbol", username_error=None, username=username)
        
        # Check if the password and confirm password values match
        elif password != confirm_password:
            return render_template("register.html", confirm_pass_error="Passwords donot match", username=username)
        else:
            # Insert the record into the users table in database
            try:
                new_user = Users(username=username, hash=generate_password_hash(password))
                db.session.add(new_user)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return render_template("register.html", username_error="Username already taken", password_error=None)

            # Redirect to login route after successful registeration
            return redirect(url_for('login'))
        
    else:
        return render_template("register.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    socketio.run(app, debug = "True")