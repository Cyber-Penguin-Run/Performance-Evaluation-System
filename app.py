from datetime import datetime, timedelta
from flask import Flask, config, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
import jwt
import functools
import random
import string
import bcrypt
from pyodbc import native_uuid
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
            return redirect(url_for("login"))

        try:
            auth_data = jwt.decode(token, app.config['JWT_KEY'], algorithms=["HS256"])
            perms = db.get_user_perms(auth_data['user_id'])
            auth_data['userPerms'] = perms[0]

        except Exception as e:
            print(e)
            return redirect(url_for("login"))

        return f(*args, **kwargs, auth_data=auth_data)

    return secure_wrapper


@app.route('/')
def index():
    return redirect("/login")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form['username']
        username = username.lower()
        password = request.form['password']
        userExists = db.get_user({"username": username})
        # print(userExists)
        if userExists is not None:
            print('user exists')
            if userExists["userPassword"] == password:
                print('login successful.')
                print(userExists)
                auth_token = jwt.encode({"user_id": userExists['userID'], "username": userExists["username"],
                                         "exp": datetime.utcnow() + timedelta(days=1)}, app.config['JWT_KEY'])
                print(auth_token)
                response = make_response(redirect("/home"))
                response.set_cookie("token", auth_token)

                return response
        else:
            return render_template('error.html'), {"Refresh": "4; url=/login"}
    return render_template('error.html'), {"Refresh": "4; url=/login"}


@app.route('/logout')
def logout():
    response = make_response(render_template('logout.html'), {"Refresh": "1; url=/login"})
    response.delete_cookie("token")
    return response


@app.route('/register', methods=["GET", "POST"])
@secure_site
def register(auth_data = None):
    print(auth_data)
    if auth_data['userPerms']['adminDashboard'] == False:
        return redirect(url_for("home_message", message="You do not have adecuate permissions for page you tried to access."))

    if request.method == "GET":
        states = db.getStates()
        families = db.get_like_families({"familyName": ""})
        return render_template("register.html", families=families, states=states)
    elif request.method == "POST":

        try:
            username = request.form['username']
            username = username.lower()
            password = request.form['password']
            address = request.form['address']
            state = request.form['state']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            phone = request.form['phoneNumber']
            email = request.form['emailAddress']
            user_role = request.form['userRole']
        except KeyError as e:
            print("Missing arguments for register.")
            return render_template('error.html'), {"Refresh": "4; url=/register"}

        new_user = {"username": username, "userPassword": password, "userAddress": address, "stateIDFK": state,
                    "firstName": firstname, "lastName": lastname, "phoneNumber": phone.strip(), "email": email,
                    "userRole": user_role}

        if user_role == "parent":
            family = request.form.get("userFamily")
            new_user['familyID'] = family

        if db.create_user(new_user):
            return "<h1>Success! you will be redirected soon!</h1>", {"Refresh": "2; url=/admin/staff"}
        else:
            return render_template('error.html'), {"Refresh": "4; url=/register"}


@app.route('/home')
@secure_site
def home(auth_data=None):
    return render_template("home.html", auth_data=auth_data)

# Home with message
@app.route('/home/<message>')
@secure_site
def home_message(message, auth_data=None):
    return render_template("home.html", auth_data=auth_data, message=message)


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

# redirect to /sessions to display table
@app.route('/sessions')
def sessions():
    session_result = db.query('SELECT* FROM studentSessions')
    return render_template('sessions.html', sessions=session_result)


# redirect to form submit
@app.route('/sessions/sessions_form', methods=['GET', 'POST'])
def sessions_form():
    if request.method == 'GET':
        return render_template('/elements/sessions_form.html')

    elif request.method == 'POST':
        program_IDFK = request.form['program_IDFK']
        session_subject = request.form['session_subject']
        session_date = request.form['session_date']
        session_hours = request.form['session_hours']
        session_attendedhours = request.form['session_attendedhours']
        student_IDFK = request.form['student_IDFK']
        staff_usersIDFK = request.form['staff_usersIDFK']

        result = db.create_session(
            {'programIDFK': program_IDFK, 'sessionSubject': session_subject, 'sessionDate': session_date,
             'sessionHours': session_hours, 'sessionAttendedhours': session_attendedhours, 'studentIDFK': student_IDFK,
             'staffUsersIDFK': staff_usersIDFK})

        return render_template('sessions.html')


####  Modular route files
import my_student
import admin_dashboard
import todos_dashboard
import testprep_dashboard
import coach_dashboard


if __name__ == '__main__':
    app.run(debug=True)
