"""Flask app."""
from flask import Flask, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

from helpers import *

# Config key-value pairs are stored in config.py
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


conn = sqlite3.connect('data.db')

try:
    conn.execute('''CREATE TABLE users
            (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL);''')
except:
    #means table already exists
    pass



# Homepage
@app.route("/")
def index():
    return render_template("index.html")

# User dashboard
@app.route("/dashboard")
@login_required
def dashboard():
    conn = sqlite3.connect('data.db')
    return render_template("dashboard.html")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    conn = sqlite3.connect('data.db')
    if request.method == "POST":
        
        email = request.form.get('email')
        
        key = request.form.get('password')
        
        if not (email and key):
            
            return render_template('Please enter an email and password!')

        if not email:
            
            return render_template('login.html', invalid = 'Please enter an email!')
        
        if not key:
            
            return render_template('login.html', invalid = 'Please enter a password!', default = {'email':email})
        
        rows = conn.execute('SELECT * FROM users WHERE email = ' +
                            '"' + request.form.get('email') + '"')
        rows = rows.fetchall()
        
        if len(rows) == 0:
            
            return render_template('login.html', invalid="Unregistered Email!", default={'email': email})
        
        else:
            
            if check_password_hash(rows[0][2], key):
                
                return render_template('dashboard.html', user = rows[0][1])
            else:
                
                return render_template('login.html', invalid = 'Invalid Password!', default={'email': email})
    else:
        
        return render_template("login.html")

#Logout
@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


# Register page
@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    conn = sqlite3.connect('data.db')
    if request.method == "POST":

        #Checking if email is valid (look at helpers.py)
        if not is_valid_email(request.form.get('email')):
            return render_template('register.html', invemail="Please enter a valid email adress", default_stuff={'email': request.form.get('email'), 'name': request.form.get('username')})

        #Checking if password is valid (look at helpers.py)
        elif not good_password(request.form.get('password')):

            return render_template('register.html', invpas="Password should contain uppercase character and a number!", default_stuff={'email': request.form.get('email'), 'name': request.form.get('username')})

        #Checking if password confirmation matches
        elif request.form.get('password') != request.form.get('confirmation'):
            
            return render_template('register.html', invpas = "Passwords don't match", default_stuff = {'email':request.form.get('email'), 'name':request.form.get('username')})
        
        elif len(request.form.get('username')) < 4:

            return render_template('register.html', invemail="Username must be at least 4 characters long!", default_stuff={'email': request.form.get('email'), 'name': request.form.get('username')})
        
        # rows = conn.execute('SELECT * FROM users WHERE username = ' + '"' + request.form.get('username') + '"')
        
        # rows = rows.fetchall()

        rows1 = conn.execute('SELECT * FROM users WHERE email = ' +
                            '"' + request.form.get('email') + '"')
        rows1 = rows1.fetchall()

        #Lets not do this since we are loggin in with email, lets let them have whatever username they want
        
        # #Means that this username already exists
        
        # if len(rows) > 0:
        
        #     return render_template('register.html', invpas="Username already exists!")
        
        if len(rows1) > 0:
           
           return render_template('register.html', invemail="Email already exists!", default_stuff={'email': request.form.get('email'), 'name': request.form.get('username')})

        else:
            #Insert user into database
            command = 'INSERT INTO users (username, password, email) VALUES (%s, %s, %s);' % (
                '"' + request.form.get('username') + '"', '"' + generate_password_hash(request.form.get('password')) + '"', '"' + request.form.get('email') + '"')
            
            conn.execute(command)
            
            conn.commit()

            rows = rows = conn.execute(
                'SELECT * FROM users WHERE username = ' + '"' + request.form.get('username') + '"')
            
            rows = rows.fetchall()
            
            session['userid'] = rows[0][0]
            
            user = rows[0][1]
            
            return render_template('dashboard.html', user = user)
        


        
    else:
        
        return render_template("register.html")


conn.commit()
