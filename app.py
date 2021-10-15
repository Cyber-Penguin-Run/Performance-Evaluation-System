from datetime import datetime, timedelta
from flask import Flask, render_template, url_for, request, flash
from flask.helpers import make_response
import jwt
import functools


app = Flask(__name__)
app.config['JWT_KEY'] ='soiqwueho28973987265362#^$%#'

def secure_site(f):
    @functools.wraps(f)
    def secure_wrapper(*args, **kwargs):

        token = request.cookies.get('token')
        
        if not token:
            return "No token provided."
        
        try:
            auth_data = jwt.decode(token, app.config['JWT_KEY'], algorithms=["HS256"])
            print(auth_data)
        except:
            return "Token invalid."

        return f(*args, **kwargs, auth_data = auth_data)
    return secure_wrapper


@app.route('/')
def index():
    return 'Hello, world!'

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username == "Braian" and password == "password":
            token = jwt.encode({"username":username, "exp":datetime.utcnow() + timedelta(hours = 24)}, app.config['JWT_KEY'])
            response = make_response(render_template("layout.html"))
            response.set_cookie("token", token.encode("UTF-8"))
            return response

@app.route('/logout')
def logout():
    return 'Logged out.'

@app.route('/home')
@secure_site
def home(auth_data = None):
    return f"{auth_data['username']} you are logged in!"

# students page with diff request methods.
# tables will be shown with editing functions add/edit/delete/etc.
# data entered will be replaced with sql information once DB is up and running.
@app.route('/students', methods=['POST','GET', 'DELETE', 'PUT'])
def students():
    if request.method=='GET':
        return render_template('students.html', studentName='John Doe', studentID='0001', subjects='Sample Text',
                               grades='Sample Text', status='Active')
    else:
        #template text showcasing an error or something in else in the future. will return an error page or something.
        return render_template('error.html', studentName='John Doe')


@app.route('/staff')
def staff():
    return 'staff'

@app.route('/portal')
def portal():
    return render_template('staffportal.html')

"""
Debug mode to run the code without having to
run it from the terminal/cmd. Please remove it during
production.
"""
if __name__=='__main__':
    app.run(debug=True)