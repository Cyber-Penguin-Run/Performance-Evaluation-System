from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
import uuid
from __main__ import app, secure_site, db

nav_columns = {"All Assignments":"assignments_all", "Quizzes":"get_quizzes", "Exams": "get_exams", "Homeworks":"get_homeworks", "Papers": "get_papers"}



#Redirect to /assignment_form to search for a student's assigments
#Returns the form submission
@app.route('/assignments/form', methods=['POST', 'GET'])
@secure_site
def assignmentform(auth_data = None):

    if request.method=='GET':    
        selected_student = request.args.get('stusearch')

        formsearch = db.query('SELECT * FROM assignments')

        results = []  
        for thing in formsearch:
            if thing['studentIDFK'] == str(selected_student):
                results.append(thing)
            
        return render_template('assignments.html', assignment_form=results, auth_data=auth_data, nav_columns= nav_columns)


@app.route('/assignments/all', methods=['GET'])
@secure_site
def assignments_all(auth_data = None):
    formsearch = db.query('SELECT * FROM assignments')
    return render_template('assignments.html', assignment_form=formsearch, auth_data=auth_data, nav_columns= nav_columns)


@app.route('/assignments/Quizzes', methods=['GET'])
@secure_site
def get_quizzes(auth_data = None):

    formsearch = db.query('SELECT * FROM assignments')

    results = []  
    for thing in formsearch:
        if thing['assignmentType'] == "Quiz":
            results.append(thing)
            
    return render_template('assignments.html', assignment_form=results, auth_data=auth_data, nav_columns= nav_columns)


@app.route('/assignments/Exams', methods=['GET'])
@secure_site
def get_exams(auth_data = None):

    formsearch = db.query('SELECT * FROM assignments')

    results = []  
    for thing in formsearch:
        if thing['assignmentType'] == "Exam":
            results.append(thing)
            
    return render_template('assignments.html', assignment_form=results, auth_data=auth_data, nav_columns= nav_columns)


@app.route('/assignments/Homeworks', methods=['GET'])
@secure_site
def get_homeworks(auth_data = None):

    formsearch = db.query('SELECT * FROM assignments')

    results = []  
    for thing in formsearch:
        if thing['assignmentType'] == "Homework":
            results.append(thing)
            
    return render_template('assignments.html', assignment_form=results, auth_data=auth_data, nav_columns= nav_columns)


@app.route('/assignments/Papers', methods=['GET'])
@secure_site
def get_papers(auth_data = None):

    formsearch = db.query('SELECT * FROM assignments')

    results = []  
    for thing in formsearch:
        if thing['assignmentType'] == "Paper":
            results.append(thing)
            
    return render_template('assignments.html', assignment_form=results, auth_data=auth_data, nav_columns= nav_columns)
