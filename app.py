# from flask import Flask, render_template, redirect, url_for, request, flash
# from models import db, User, Event, RSVP
# from flask_login import LoginManager, login_user, logout_user, login_required
# from utils import generate_analytics

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'supersecretkey'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_manager.db'
# db.init_app(app)

# login_manager = LoginManager()
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # Handle the login form submission
#         username = request.form.get('username')
#         password = request.form.get('password')
#         # Process login (authenticate user, etc.)
#         return "Logged in successfully"
#     return render_template('login.html')  # Return the login form on GET request

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         # Handle the form submission
#         username = request.form.get('username')
#         password = request.form.get('password')
#         # Process the data, e.g., store it in the database
#         return "Form submitted successfully"
#     return render_template('register.html')


# @app.route('/')
# def index():
#     return render_template('/index.html')

# @app.route('/dashboard')
# @login_required
# def dashboard():
#     events = Event.query.all()
#     analytics = generate_analytics(events)
#     return render_template('dashboard.html', events=events, analytics=analytics)

# # Additional routes for login, register, create_event, RSVP, etc.

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Configurations directly in the app
app.config['MYSQL_HOST'] = 'localhost'  # Change if your MySQL is on a different host
app.config['MYSQL_USER'] = 'mysql_user'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'database'
app.config['SECRET_KEY'] = os.urandom(24)

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        user = cur.fetchone()

        if user:
            flash('Username already exists. Please choose another one.', 'error')
        else:
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            mysql.connection.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))

        cur.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        user = cur.fetchone()

        if user and check_password_hash(user[2], password):  # assuming password is at index 2
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials, please try again.', 'error')

        cur.close()

    return render_template('login.html')

if __name__ == "__main__":
    app.run(host="192.168.88.132", port=80, debug=True)
