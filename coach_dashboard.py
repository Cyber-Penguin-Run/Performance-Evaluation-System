import re
from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
from app import app, secure_site, db

nav_columns = {"Coach Overview":"coach_home", "Personal Information":"coach_info", "Assignments":"coach_assignments"}

@app.route("/coach/overview", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def coach_home(auth_data = None):
    coach = db.get_coach_information(auth_data['user_id'])
    return render_template("coach_overview.html", auth_data = auth_data, nav_columns = nav_columns, coach = coach[0])

@app.route("/coach/info", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def coach_info(auth_data = None):
    if request.method == 'GET':

            states = db.getStates()
            coach = db.get_coach_information(auth_data['user_id'])
            return render_template('coach_info.html', auth_data=auth_data, nav_columns=nav_columns, states=states, coach=coach[0])

    elif request.method == 'POST':
        print(request.form)
        Fname = request.form.get('firstname')
        Lname = request.form.get('lastname')
        address = request.form.get("address")
        phone = request.form.get('phoneNumber')
        email = request.form.get('email')
        state = request.form.get("state")
        country = request.form.get("country")

        if db.update_coach_information(auth_data['user_id'], {"firstName": Fname, "lastName":Lname,
        "userAddress":address, "phoneNumber":phone, "email":email, "stateIDFK":state}):
            print("Successful update")

        states = db.getStates()
        coach = db.get_coach_information(auth_data['user_id'])

        return render_template('coach_info.html', auth_data=auth_data, nav_columns=nav_columns, states=states, coach=coach[0])


@app.route("/coach/assignments", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def coach_assignments(auth_data = None):
    if auth_data['userPerms']['adminDashboard']:
        assignments = db.get_coach_assignments("")
        print(assignments) 
    else:
        assignments = db.get_coach_assignments(auth_data['user_id'])

    assignmentTypes = [assignment['assignmentType'] for assignment in db.query("SELECT DISTINCT assignmentType FROM assignments") if len(assignment['assignmentType']) > 0]

    return render_template("coach_assignments.html", auth_data=auth_data, nav_columns=nav_columns, assignments=assignments, assignmentTypes=assignmentTypes)


@app.route('/coach/assignments/<selectedType>', methods=['GET'])
@secure_site
def filter_assignments(selectedType, auth_data = None):

    assignments = db.query(f"SELECT * FROM assignments WHERE assignmentType = '{selectedType}'") 

    assignmentTypes = [assignment['assignmentType'] for assignment in db.query("SELECT DISTINCT assignmentType FROM assignments") if len(assignment['assignmentType']) > 0]

    return render_template("coach_assignments.html", auth_data=auth_data, nav_columns=nav_columns, assignments=assignments, assignmentTypes=assignmentTypes)