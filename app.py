import sys
from datetime import datetime, timedelta
<<<<<<< HEAD
import MySQLdb
import data as data
import pyodbc
import self as self
from flask import Flask, json, render_template, url_for, request, redirect, jsonify
=======
from flask import Flask, config, json, render_template, url_for, request, redirect, jsonify
>>>>>>> origin/api
from flask.helpers import make_response
import jwt
import functools
import random
import string
import bcrypt

import connection
from connection import Database

app = Flask(__name__)
app.config['JWT_KEY'] = 'soiqwueho28973987265362#^$%#'

# Connecting to the database
db = Database()


@app.context_processor
def handle_context():
    '''Inject object into jinja2 templates.'''
    return dict(jsonify=jsonify)


def secure_site(f):
    @functools.wraps(f)
    def secure_wrapper(*args, **kwargs):

        token = request.cookies.get('token')

        if not token:
            return "No token provided."

        try:
            auth_data = jwt.decode(token, app.config['JWT_KEY'], algorithms=["HS256"])
        except:
            return "Token invalid."

        return f(*args, **kwargs, auth_data=auth_data)

    return secure_wrapper


@app.route('/')
def index():
    return 'This is the index page for the Enrichery web app.'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        userExists = db.get_user({"username": username})
        # print(userExists)
        if userExists is not None:
            print('user exists')
            if userExists["userPassword"] == password:
                print('login successful.')
                auth_token = jwt.encode({"user_id":userExists['userID'], "username":userExists["username"], "exp":datetime.utcnow() + timedelta(days=1)}, app.config['JWT_KEY'])

                response = make_response(redirect("/home"))
                response.set_cookie("token", auth_token)

                return response
        else:
            return render_template('error.html'), {"Refresh": "4; url=/login"}


@app.route('/logout')
def logout():
    return 'You have been logged out.'


# redirect to /register
@app.route('/register', methods=["GET", "POST"])
def register():
    states = db.getStates()
    if request.method == "GET":
        return render_template("register.html", states=states)
    elif request.method == "POST":
        username = request.form['username']
        username.lower()
        password = request.form['password']
        address = request.form['address']
        state = request.form['state']
        if db.create_user({"username": username, "userPassword": password, "userAddress": address, "stateIDFK": state}):
            return "<h1>Success! you will be redirected soon!</h1>", {"Refresh": "4; url=/login"}
        else:
            return render_template('error.html'), {"Refresh": "4; url=/register"}


# display home directory
@app.route('/home')
@secure_site
<<<<<<< HEAD
def home(auth_data=None):
    return f"{auth_data['username']} you are logged in!"
=======
def home(auth_data = None):
    return render_template("home.html", auth_data=auth_data)
>>>>>>> origin/api


# students page with diff request methods.
# tables will be shown with editing functions add/edit/delete/etc.
# data entered will be replaced with sql information once DB is up and running.
@app.route('/students', methods=['POST', 'GET', 'DELETE', 'PUT'])
def students():
    if request.method == 'GET':
        return render_template('students.html', studentName='John Doe', studentID='0001', subjects='Sample Text',
                               grades='Sample Text', status='Active')
    else:
        # template text showcasing an error or something in else in the future. will return an error page or something.
        return render_template('error.html', studentName='John Doe')


# redirect to /coaches to display table
@app.route('/coaches')
def staff():
    return 'coaches'


# redirect to /assignments to display table
@app.route('/assignments')
def assignments():
    assignment_result = db.query(sql='SELECT* FROM assignments')
    return render_template('assignments.html', assignments=assignment_result)


# redirect to /sessions to display table
@app.route('/sessions')
def sessions():
    session_result = db.query(sql='SELECT* FROM studentSessions')
    return render_template('sessions.html', sessions=session_result)


@app.route('/sessions_form', methods=['GET', 'POST'])
def createSessions():
    if request.method == 'GET':
        return render_template('createSessions.html')

    elif request.method == 'POST':
        session_ID = request.form['session_ID']
        program_IDFK = request.form['program_IDFK']
        session_subject = request.form['session_subject']
        session_date = request.form['session_date']
        session_hours = request.form['session_hours']
        session_attendedhours = request.form['session_attendedhours']
        student_IDFK = request.form['student_IDFK']
        staff_usersIDFK = request.form['student_IDFK']
        if db.create_sessions({"session_ID": session_ID, "program_IDFK": program_IDFK,
                               "session_subject": session_subject,
                               "session_date": session_date, "session_hours": "session_hours",
                               session_hours: session_hours, "session_attendedhours:":
                                   session_attendedhours, "student_IDFK": student_IDFK,
                               "staff_usersIDFK": staff_usersIDFK}):
            return "<h1>Success! you will be redirected soon!</h1>", {"Refresh": "4; url=/login"}
        else:
            return render_template('error.html'), {"Refresh": "4; url=/register"}


@app.route('/states')
def states():
    state_result = db.query(sql='SELECT* FROM states')
    return render_template('states.html', state=state_result)


"""""
Debug mode to run the code without having to
run it from the terminal/cmd. Please remove it during
production.
"""
if __name__ == '__main__':
    app.run(debug=True)
