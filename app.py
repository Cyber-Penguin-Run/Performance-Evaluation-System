from flask import Flask, render_template, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] =''

@app.route('/')
def index():
    return 'Hello'

@app.route('/login')
def login():
    return 'world'

@app.route('/home')
def home():
    return 'home'

@app.route('/students')
def students():
    return 'students'

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