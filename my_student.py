import re
from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from app import assignments, sessions
from connection import Database
from __main__ import app, secure_site, db

nav_columns = {"Students":"mystudent_students", "Family":"mystudent_families"}

@app.route("/mystudent/overview", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def mystudent_overview(auth_data = None):
    return render_template("mystudent_overview.html", auth_data=auth_data, nav_columns=nav_columns)

@app.route("/mystudent/students", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def mystudent_students(auth_data = None):
    if request.method == "GET":
        if auth_data['userPerms']['adminDashboard']:
            students = db.query("SELECT * FROM student")
        else:
            students = db.get_coach_students(auth_data['user_id'])
        return render_template("mystudent_students.html", auth_data=auth_data, nav_columns=nav_columns, students = students)


    if request.method == "POST":
        fullname = request.form.get("fullname")
        print(fullname)
        if auth_data['userPerms']['adminDashboard']:
            students = db.get_coach_students_fullname("", fullname)
        else:
            students = db.get_coach_students(auth_data['user_id'], fullname)
        return render_template("mystudent_students.html", auth_data=auth_data, nav_columns=nav_columns, students = students)


@app.route("/mystudent/students/<studentID>", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def mystudent_student_info(studentID, auth_data = None):
    
    if request.method == "GET":
        try:
            student_info = db.get_student(studentID)[0]
        except KeyError:
            return render_template("mystudent_student_info.html", auth_data=auth_data, nav_columns=nav_columns, message = "Student is not valid.", student_info={"assignments":[]})

        student_info['assignments'] = db.get_student_assignments(studentID)
        student_info['sessions'] = db.get_student_sessions(studentID)

        return render_template("mystudent_student_info.html", auth_data=auth_data, nav_columns=nav_columns, student_info=student_info)

    if request.method == "POST":
        if request.form['submitBtn'] == "addAssignment":
            return redirect(f"/mystudent/assignment/add/{studentID}")
        return render_template("mystudent_student_info.html", auth_data=auth_data, nav_columns=nav_columns, message = "Student is not valid.", student_info={"assignments":[]})


@app.route("/mystudent/assignment/add/<studentID>", methods=["POST", "GET"])
@secure_site
def mystudent_student_assignment(studentID, auth_data = None):
    if request.method == "GET":
        return render_template('/elements/assignments_form.html', auth_data = auth_data, nav_columns=nav_columns)
    if request.method == "POST":
        assignment_info = request.form
        if db.create_assignment(auth_data['user_id'], studentID, assignment_info):
            return redirect(f"/mystudent/students/{studentID}")
        return redirect(f"/mystudent/students/{studentID}")


@app.route("/mystudent/families", methods = ["POST", "GET"])
@secure_site
def mystudent_families(auth_data = None):
    if request.method == "GET":
        if auth_data['userPerms']['adminDashboard']:
            families = db.get_coach_families("")
        else:
            families = db.get_coach_families(auth_data['user_id'])

        return render_template("mystudent_families.html", auth_data=auth_data, nav_columns=nav_columns, families=families)

    if request.method == "POST": 
        if auth_data['userPerms']['adminDashboard']:
            families = db.get_coach_like_families("", request.form['familyName'])
        else:
            families = db.get_coach_like_families(auth_data['user_id'], request.form['familyName'])

        return render_template("mystudent_families.html", auth_data=auth_data, nav_columns=nav_columns, families=families)




@app.route("/mystudent/families/<familyID>", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def mystudent_family_info(familyID, auth_data = None):
    if request.method == "GET":
        family = db.get_family(familyID)
        
        return render_template("/elements/family_display.html", auth_data=auth_data, nav_columns=nav_columns, family=family)
    
    if request.method == "POST":
        return redirect("/mystudent/families")