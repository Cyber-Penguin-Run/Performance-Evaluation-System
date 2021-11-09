import random
import uuid

from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
from __main__ import app, secure_site, db

nav_columns = {"Change Todo List":"todos_form"}


@app.route("/todos", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def todos(auth_data = None):
    todos_table = db.query('Select * FROM todos')
    return render_template('todos.html', auth_data = auth_data, nav_columns=nav_columns, todos_table=todos_table)

@app.route("/todos_form", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def todos_form(auth_data = None):
    todos_table = db.query('Select * FROM todos')
    #todoID = uuid.uuid
    if request.method == 'POST':
        description = request.form['todoDescription']
        db.create_todo(description)
        return render_template('success.html'), {"Refresh": "4; url=/todos"}
    return render_template('/elements/todos_form.html', auth_data = auth_data, nav_columns=nav_columns, todos_table=todos_table)
