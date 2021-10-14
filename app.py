from flask import Flask, render_template, url_for, request, flash
app = Flask(__name__)
app.config['SECRET_KEY'] =''

@app.route('/')
def index():
    return 'Hello, world!'

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/logout')
def logout():
    return 'Logged out.'

@app.route('/home')
def home():
    return render_template('layout.html')

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

"""
Debug mode to run the code without having to
run it from the terminal/cmd. Please remove it during
production.
"""
if __name__=='__main__':
    app.run(debug=True)