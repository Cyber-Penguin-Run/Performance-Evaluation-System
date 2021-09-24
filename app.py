from flask import Flask, render_template, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] =''

@app.route('/')
def home():
    return render_template()

@app.login('/login')
def login():
    return



"""
Debug mode to run the code without having to
run it from the terminal/cmd. Please remove it during
production.
"""
if __name__=='__main__':
    app.run(debug=True)