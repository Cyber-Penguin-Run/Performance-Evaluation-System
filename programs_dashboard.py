from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
from __main__ import app, secure_site, db

nav_columns = {'College Workshop':'programs_college_summer_workshop','Academic Coaching':'programs_academic_coaching',
               'College Coaching': 'programs_college_coaching', 'Education Future':'programs_education_future',
               'Executive Function':'programs_exec_function', 'Executive Function Mini':'programs_exec_function_mini',
               'Small Groups':'programs_small_groups','Study Spot':'programs_study_spot',
               'Program Test Prep':'programs_test_prep'
               }

@app.route("/programs/overview", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def programs_overview(auth_data = None):
    if request.method == 'GET':
        return render_template('studentPrograms.html',auth_data=auth_data, nav_columns= nav_columns)


@app.route('/programs/CollegeSummerWorkshop', methods = ['GET','POST','PUT','DELETE'])
@secure_site
def programs_college_summer_workshop(auth_data=None):
    if request.method == 'GET':
        return render_template('programs_form.html',auth_data=auth_data)


@app.route('/programs/Academic_Coaching', methods = ['GET','POST','PUT','DELETE'])
@secure_site
def programs_academic_coaching(auth_data=None):
    if request.method == 'GET':
        return render_template('programs_form.html',auth_data=auth_data)


@app.route('/programs/College_Coaching', methods = ['GET','POST','PUT','DELETE'])
@secure_site
def programs_college_coaching(auth_data=None):
    if request.method == 'GET':
        return render_template('programs_form.html',auth_data=auth_data)


@app.route('/programs/Education_Future', methods = ['GET','POST','PUT','DELETE'])
@secure_site
def programs_education_future(auth_data=None):
    if request.method == 'GET':
        return render_template('programs_form.html',auth_data=auth_data)


@app.route('/programs/Exec_Function', methods = ['GET','POST','PUT','DELETE'])
@secure_site
def programs_exec_function(auth_data=None):
    if request.method == 'GET':
        return render_template('programs_form.html',auth_data=auth_data)


@app.route('/programs/Exec_Function_Mini', methods = ['GET','POST','PUT','DELETE'])
@secure_site
def programs_exec_function_mini(auth_data=None):
    if request.method == 'GET':
        return render_template('programs_form.html',auth_data=auth_data)


@app.route('/programs/Small_Groups', methods = ['GET','POST','PUT','DELETE'])
@secure_site
def programs_small_groups(auth_data=None):
    if request.method == 'GET':
        return render_template('programs_form.html',auth_data=auth_data)


@app.route('/programs/Study_Spot', methods = ['GET','POST','PUT','DELETE'])
@secure_site
def programs_study_spot(auth_data=None):
    if request.method == 'GET':
        return render_template('programs_form.html',auth_data=auth_data)


@app.route('/programs/Test_Prep', methods = ['GET','POST','PUT','DELETE'])
@secure_site
def programs_test_prep(auth_data=None):
    if request.method == 'GET':
        return render_template('programs_form.html',auth_data=auth_data)
