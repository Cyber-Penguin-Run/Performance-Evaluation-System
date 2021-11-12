from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
import uuid
from app import app, secure_site, db

nav_columns = {"Coach Overview":"coach_home", "Personal Information":"coach_info", "Assignments":"coach_assignments"}


@app.route('/coach/assignments')
def assignments(auth_data = None):
    nav_columns = {"Overview":"admin_overview", "Staff":"admin_staff", "Families":"admin_families", "Business":"admin_business"}
    selectedtype = "All Assignments"
    assignment_result = db.query(sql='SELECT* FROM assignments')
    return render_template('assignments.html', selectedtype=selectedtype, assignments_form=assignment_result, auth_data=auth_data, nav_columns=nav_columns)


#Redirect to /assignment_form to search for a student's assigments
#Returns the form submission
@app.route('/coach/assignments/form', methods=['POST', 'GET'])
@secure_site
def assignmentform(auth_data = None):

    if request.method=='GET':    
        selected_student = request.args.get('stusearch')

        formsearch = db.query('SELECT * FROM assignments')

        results = []  
        for thing in formsearch:
            if thing['studentIDFK'] == str(selected_student):
                results.append(thing)
            
        return render_template('coach_assignments.html', selectedtype=selectedtype, assignment_form=results, auth_data=auth_data, nav_columns= nav_columns)


@app.route('/coach/assignments/all', methods=['GET'])
@secure_site
def assignments_all(auth_data = None):
    selectedtype = "All Assignments"

    formsearch = db.query('SELECT * FROM assignments')
    return render_template('coach_assignments.html', selectedtype=selectedtype, assignment_form=formsearch, auth_data=auth_data, nav_columns= nav_columns)


@app.route('/coach/assignments/quizzes', methods=['GET'])
@secure_site
def get_quizzes(auth_data = None):

    formsearch = db.query('SELECT * FROM assignments')
    selectedtype = "Quizzes"

    results = []  
    for thing in formsearch:
        if thing['assignmentType'] == "Quiz":
            results.append(thing)
            
    return render_template('coach_assignments.html', selectedtype=selectedtype, assignment_form=results, auth_data=auth_data, nav_columns= nav_columns)


@app.route('/coach/assignments/exams', methods=['GET'])
@secure_site
def get_exams(auth_data = None):
    selectedtype = "Exams"

    formsearch = db.query('SELECT * FROM assignments')

    results = []  
    for thing in formsearch:
        if thing['assignmentType'] == "Exam":
            results.append(thing)
            
    return render_template('coach_assignments.html', selectedtype=selectedtype, assignment_form=results, auth_data=auth_data, nav_columns= nav_columns)


@app.route('/coach/assignments/homeworks', methods=['GET'])
@secure_site
def get_homeworks(auth_data = None):
    selectedtype = "Homeworks"

    formsearch = db.query('SELECT * FROM assignments')

    results = []  
    for thing in formsearch:
        if thing['assignmentType'] == "Homework":
            results.append(thing)
            
    return render_template('coach_assignments.html', selectedtype=selectedtype, assignment_form=results, auth_data=auth_data, nav_columns= nav_columns)


@app.route('/coach/assignments/papers', methods=['GET'])
@secure_site
def get_papers(auth_data = None):
    selectedtype = "Papers"

    formsearch = db.query('SELECT * FROM assignments')
    print(formsearch)
    results = []  
    for thing in formsearch:
        if thing['assignmentType'] == "Paper":
            results.append(thing)
            
    return render_template('coach_assignments.html',selectedtype=selectedtype,  assignment_form=results, auth_data=auth_data, nav_columns= nav_columns)
