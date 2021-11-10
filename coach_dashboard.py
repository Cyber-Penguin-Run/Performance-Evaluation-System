from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
from __main__ import app, secure_site, db

nav_columns = {"Coach Overview":"coach_home", "Personal Information":"coach_info", "Assignments":"coach_assignments"}

@app.route("/coach/overview", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def coach_home(auth_data = None):
    return render_template("coach_overview.html", auth_data = auth_data, nav_columns = nav_columns)

@app.route("/coach/info", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def coach_info(auth_data = None):
    coach_table = db.query('SELECT * FROM staff')
    specific_coach = db.query("SELECT * FROM staff WHERE userIDFK = ('03762ebe90034818a82fcd011f6389ea')")
    return render_template('coaches.html', auth_data=auth_data, nav_columns=nav_columns, coach_table=coach_table, specific_coach=specific_coach)

@app.route("/coach/assignments", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def coach_assignments(auth_data = None):
    if auth_data['userPerms']['adminDashboard']:
        assignments = db.get_coach_assignments("")
    else:
        assignments = db.get_coach_assignments(auth_data['user_id'])

    return render_template("coach_assignments.html", auth_data=auth_data, nav_columns=nav_columns, assignments=assignments)
