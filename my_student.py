from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
from __main__ import app, secure_site, db

nav_columns = {"Overview":"/mystudent/overview", "Students":"/mystudent/students", "Family":"/mystudent/family"}

@app.route("/mystudent/overview", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def mystudent_overview(auth_data = None):
    return render_template("mystudent_overview.html", auth_data=auth_data)

@app.route("/mystudent/students", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def mystudent_students(auth_data = None):
    return render_template("students.html", auth_data=auth_data)

@app.route("/mystudent/family", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def mystudent_family(auth_data = None):
    return "/mystudent/family"