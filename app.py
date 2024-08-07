from flask import Flask, redirect, session, render_template, flash, request, url_for, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from functools import wraps
import re

# Configure application
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure database connection
db = SQL("sqlite:///clubroom.db")

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
        
        rows = db.execute("SELECT * FROM users where username = ?", username)
        if len(rows) != 1:
            return render_template("login.html", username_error="Username not found")
        
        elif not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", password_error="Wrong Password")
        
        else:
            session["user_id"] = rows[0]["id"]
            return("/")
    else:
        return render_template("login.html")

# Main route / index route
@app.route('/')
@app.route('/index')
@login_required
def index():
    return "Hello"


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
        elif not re.match("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%#?&])[A-Za-z\d@$!%*#?&]{8,}$", password):
            return render_template("register.html", password_error="Must include atleast one character, number, special symbol", username_error=None, username=username)
        
        # Check if the password and confirm password values match
        elif password != confirm_password:
            return render_template("register.html", confirm_pass_error="Passwords donot match", username=username)
        else:
            # Insert the record into the users table in database
            try:
                db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))
            except ValueError:
                return render_template("register.html", username_error="Username already taken", password_error=None)

            # Redirect to login route after successful registeration
            return redirect(url_for('login'))
        
    else:
        return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)