from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
from __main__ import app, secure_site, db

nav_columns = {"Overview":"admin_overview", "Staff":"admin_staff", "Families":"admin_families", "Business":"admin_business"}



#Redirect to /assignment_form to search for a student's assigments
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
                

        return render_template('assignments.html', assignmentform=results, auth_data=auth_data, nav_columns= nav_columns)


    elif request.method =='POST':
        return render_template('assignments.html',auth_data=auth_data)