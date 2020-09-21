"""Flask app."""
from flask import Flask, render_template, request, session, redirect
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
            email TEXT NOT NULL,
            currency TEXT NOT NULL DEFAULT 'USD');''')
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

    rows = conn.execute('SELECT * FROM users WHERE id = ' +
                        '"' + str(session["userid"]) + '"')
    rows = rows.fetchall()

    info = {'balance': convert(10000, session['curr']), 'bills': convert(
        10000, session['curr']), 'food': convert(10000, session['curr']), 'shopping': convert(10000, session['curr']), 'savings': convert(10000, session['curr']), 'other': convert(10000, session['curr'])}

    return render_template("dashboard.html", user = rows[0][1], info=info)

#Settings page

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        conn = sqlite3.connect('data.db')
        if request.form.get('currency'):
            command = 'UPDATE users SET currency = "' + request.form.get('currency') + '"' + ' WHERE id = ' + str(session['userid']) +';'
            conn.execute(command)
            conn.commit()
            session['curr'] = convert_currency(request.form.get('currency'))
            return render_template('settings.html', currency = session["curr"], saved = 'Saved!')
        
        elif request.form.get('current'):
            
            command = f"SELECT * FROM users WHERE id = " + str(session['userid']) + ';'
            rows = conn.execute(command)
            rows = rows.fetchall()
            if not check_password_hash(rows[0][2], request.form.get('current')):
                return render_template('settings.html', currency = session['curr'], invcur = 'Invalid current password!')
            elif request.form.get('password') == request.form.get('current'):
                return render_template('settings.html', currency = session['curr'], invnew = 'New password cannot be the same as the old password!')
            elif not good_password(request.form.get('password')):
                return render_template('settings.html', currency = session['curr'], invnew = 'Your password must contain one uppercase character and a number!')
            elif request.form.get('password') != request.form.get('confirmation'):
                return render_template('settings.html', currency = session['curr'], invconf = 'New passwords must match!')
            else:
                command = 'UPDATE users SET password = "' + generate_password_hash(request.form.get('password')) + '" WHERE id = ' + str(session['userid']) + ';'
                conn.execute(command)
                conn.commit()
                return render_template('settings.html', currency = session['curr'], savedpass = 'Saved!')


    else:
        return render_template('settings.html', currency = session["curr"])

# Income Page
@app.route("/income", methods=["GET","POST"])
def income():
    if request.method == "POST":
        #All of the logic needed
        return 0
    else:
        return render_template('income.html')

# Expenses Page
@app.route("/expenses", methods=["GET","POST"])
def expenses():
    if request.method == "POST":
        #All of the logic needed
        return 0
    else:
        return render_template('expenses.html')



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

                session["userid"] = rows[0][0]
                session["curr"] = convert_currency(rows[0][4])
                
                return redirect('/dashboard')
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
        
        if len(rows1) > 0:
           
           return render_template('register.html', invemail="Email already exists!", default_stuff={'email': request.form.get('email'), 'name': request.form.get('username')})

        else:
            #Insert user into database
            command = 'INSERT INTO users (username, password, email) VALUES (%s, %s, %s);' % (
                '"' + request.form.get('username') + '"', '"' + generate_password_hash(request.form.get('password')) + '"', '"' + request.form.get('email') + '"')
            
            conn.execute(command)
            
            conn.commit()

            rows = conn.execute(
                'SELECT * FROM users WHERE email = ' + '"' + request.form.get('email') + '"')
            
            rows = rows.fetchall()
            
            session['userid'] = rows[0][0]
            
            session['curr'] = convert_currency(rows[0][4])

            user = rows[0][1]
            
            return redirect('/dashboard')
        


        
    else:
        
        return render_template("register.html")

@app.route('/quicklog', methods=['GET', 'POST'])
def quicklog(): 
    session.clear()
    conn = sqlite3.connect('data.db')

    rows = conn.execute('SELECT * FROM users WHERE email = ' +
                        '"' + 'umsorrytest@gmail.com' + '"')
    rows = rows.fetchall()
    print(rows)
    session["userid"] = rows[0][0]
    session["curr"] = convert_currency(rows[0][4])
    

    return redirect('/dashboard')

conn.commit()