import random
import uuid

from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
from __main__ import app, secure_site, db

nav_columns = {"Todos":"todos","Change Todo List":"todos_form"}


@app.route("/todos", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def todos(auth_data = None):
    todos_table = db.query("Select * FROM todos WHERE staffUsersID = '%s'" % auth_data['user_id'])
    return render_template('todos.html', auth_data = auth_data, nav_columns=nav_columns, todos_table=todos_table)

@app.route("/todos_form", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def todos_form(auth_data = None):
    #todos_table = db.query("Select * FROM todos WHERE staffUsersID = '%s'" % auth_data['user_id'])
    if request.method == 'POST':
        description = request.form['todoDescription']
        staffID = auth_data['user_id']
        result = db.create_todo(staffID,description)
        if result == True:
            return render_template('layout.html'), {"Refresh": "2; url=/todos"}
    return render_template('/elements/todos_form.html', auth_data = auth_data, nav_columns=nav_columns)

@app.route("/todos/delete/<todoID>", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def todo_delete(todoID,auth_data = None):
    print('deleted')
    isdeleted = db.delete_todo(todoID)
    todos_table = db.query("Select * FROM todos WHERE staffUsersID = '%s'" % auth_data['user_id'])
    if isdeleted:
        return render_template('todos.html',auth_data=auth_data, nav_columns=nav_columns,
                               message='deleted successfully',todos_table=todos_table)
    else:
        return render_template('todos.html',auth_data=auth_data, nav_columns=nav_columns,
                               message='error while deleting',todos_table=todos_table)

@app.route("/todos/update/<todoID>", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def todo_update(todoID,auth_data = None):
    if request.method == 'GET':
        todo = db.query("SELECT * FROM todos WHERE todoID = '%s'" % todoID)
        print(todo[0])
        return render_template('/elements/todos_form.html',auth_data=auth_data,
                               nav_columns=nav_columns,todoDescription=todo[0]['toDoDescription'])
    if request.method=='POST':
        print('updated')
        description = request.form.get('todoDescription')
        isupdated = db.update_todo(description,todoID)
        todos_table = db.query("Select * FROM todos WHERE staffUsersID = '%s'" % auth_data['user_id'])
        if isupdated:
            return render_template('todos.html', auth_data=auth_data, nav_columns=nav_columns,
                                   message='updated successfully', todos_table=todos_table)
        else:
            return render_template('todos.html', auth_data=auth_data, nav_columns=nav_columns,
                                   message='error while updating', todos_table=todos_table)
