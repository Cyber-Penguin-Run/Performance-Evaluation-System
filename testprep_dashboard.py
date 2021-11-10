from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
from __main__ import app, secure_site, db

nav_columns = {'Mock ACT':'mockACT','Mock SAT':'mockSAT','Mock HSPT':'mockHSPT','Mock ISEE':'mockISEE'}

@app.route("/testprep", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def testprep(auth_data = None):
    return render_template('test_prep_dashboard.html', auth_data = auth_data, nav_columns=nav_columns)

@app.route("/testprep/mockACT", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def mockACT(auth_data = None):
    if request.method=='GET':
        act_select = db.query('SELECT * FROM mockActScores left join student ON mockActScores.studentIDFK=student.studentID')
        return render_template('mockActScores.html', auth_data = auth_data, nav_columns=nav_columns,
                               act_select=act_select)

@app.route("/testprep/mockSAT", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def mockSAT(auth_data = None):
    if request.method == 'GET':
        sat_select = db.query('SELECT * FROM mockSatScores left join student ON mockSatScores.studentIDFK=student.studentID')
        return render_template('mockSatScores.html', auth_data = auth_data, nav_columns=nav_columns,
                               sat_select=sat_select)

@app.route("/testprep/mockHSPT", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def mockHSPT(auth_data = None):
    if request.method == 'GET':
        hspt_select = db.query('SELECT * FROM mockHsptScores left join student ON mockHsptScores.studentIDFK=student.studentID')
        return render_template('mockHsptScores.html', auth_data = auth_data, nav_columns=nav_columns,hspt_select=hspt_select)

@app.route("/testprep/mockISEE", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def mockISEE(auth_data = None):
    if request.method == 'GET':
        isee_select = db.query('SELECT * FROM mockIseeScores left join student ON mockIseeScores.studentIDFK=student.studentID')
        return render_template('mockIseeScores.html', auth_data = auth_data, nav_columns=nav_columns,isee_select=isee_select)

