from flask import Flask, redirect, session, render_template, flash, request
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from functools import wraps

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['TEMPLATES_AUTO_RELOAD'] = True

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
        return "<h1>SAW HER IN YOUR DREAM TODAY?<h1>"
    else:
        return render_template("login.html")

# Main route / index route
@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html")


