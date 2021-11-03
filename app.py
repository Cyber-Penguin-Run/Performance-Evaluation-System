from flask import Flask, render_template, url_for, request
import pyodbc



app = Flask(__name__)
app.config['SECRET_KEY'] =''

@app.route('/')
def index():
    return 'Hello'

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/sessions')
def sessions():
    return render_template('sessions.html')

@app.route('/assignments')
def assignments():
    return render_template('assignments.html')








#defining a route for students page with post and get methods. Delete method will be added later on but this is basis.
@app.route('/students', methods=['POST','GET'])
def students():
    #defining of error as temp holder for page response in case it is needed. this can be taken out if error testing is not required later on.
    error = None
    #if a get request then it returns a basic students.html page
    if request.method=='GET':
        return render_template('students.html')
    #else it will return error and print out a status code
    else:
        #template text showcasing an error or something in else in the future. will return an error page or something.
        return '<h1> Error with retrieval.</>'



@app.route('/staff')
def staff():
    return 'hello world'

"""
Debug mode to run the code without having to
run it from the terminal/cmd. Please remove it during
production.
"""
if __name__=='__main__':
    app.run(debug=False)