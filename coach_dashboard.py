from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
from __main__ import app, secure_site, db

nav_columns = {"Home":"coach_home", "Personal Information":"coach_info", "Student Assignments":"assignments"}

@app.route("/coach/overview", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def coach_home(auth_data = None):
    return render_template("coach_overview.html", auth_data = auth_data, nav_columns = nav_columns)

@app.route("/coach/info", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def coach_info(auth_data = None):
    return "/coach/info"