from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
from __main__ import app, secure_site, db

@app.route("/todos", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def todos(auth_data = None):
    if request.method=='GET':
        return render_template('todos.html', auth_data = auth_data)