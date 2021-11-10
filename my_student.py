from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
from __main__ import app, secure_site, db

nav_columns = {"Overview":"mystudent_overview", "Students":"mystudent_students", "Family":"mystudent_family"}

@app.route("/mystudent/overview", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def mystudent_overview(auth_data = None):
    return render_template("mystudent_overview.html", auth_data=auth_data, nav_columns=nav_columns)

@app.route("/mystudent/students", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def mystudent_students(auth_data = None):
    if auth_data['userPerms']['adminDashboard']:
        students = db.query("SELECT * FROM student")
    else:
        students = db.get_coach_students(auth_data['user_id'])
    return render_template("mystudent_students.html", auth_data=auth_data, nav_columns=nav_columns, students = students)

@app.route("/mystudent/family", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def mystudent_family(auth_data = None):
    return "/mystudent/family"