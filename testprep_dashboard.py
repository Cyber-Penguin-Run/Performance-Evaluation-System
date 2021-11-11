from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
import uuid
from __main__ import app, secure_site, db

nav_columns = {'Add Mock':'testprep','Mock ACT':'mockACT','Mock SAT':'mockSAT','Mock HSPT':'mockHSPT','Mock ISEE':'mockISEE'}

@app.route("/testprep", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def testprep(auth_data = None):
    if request.method == 'GET':
        students = db.query("SELECT * FROM student")
        return render_template('test_prep_dashboard.html', auth_data = auth_data, nav_columns=nav_columns, students=students)
    if request.method =='POST':
        fullname = request.form.get("fullname")
        print(fullname)
        if auth_data['userPerms']['adminDashboard']:
            students = db.get_coach_students_fullname("", fullname)
        else:
            students = db.get_coach_students(auth_data['user_id'], fullname)
    return render_template("/elements/mock_exam_form.html", auth_data=auth_data, nav_columns=nav_columns, students=students)

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

@app.route("/testprep/change/<studentID>", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def change(studentID,auth_data = None):
    if request.method == 'GET':
        isee_select = db.query('SELECT * FROM mockIseeScores left join student ON mockIseeScores.studentIDFK=student.studentID')
        return render_template('/elements/mock_exam_form.html', auth_data = auth_data, nav_columns=nav_columns,
                               isee_select=isee_select)

    if request.method == 'POST':
        #for primary key generation
        if 'actButton' in request.form.keys():
            print(request.form)
            testscores = 36
            english = request.form['englishScore']
            math = request.form['mathScore']
            reading = request.form['readingScore']
            science = request.form['scienceScore']
            actComp = request.form['actCompScore']
            actType = request.form['actType']
            actTestDate = request.form['actTestDate']
            if db.create_mock(mockType='act', mockInfo={'studentIDFK':studentID,'englishScore':english,'englishMax':testscores,
                                                     'mathScore':math,'mathMax':testscores,'readingScore':reading,
                                                     'readingMax':testscores,'scienceScore':science,'scienceMax':testscores,
                                                     'actCompScore':actComp,'actType':actType,'actTestDate':actTestDate}):
                return render_template('/elements/mock_exam_form.html', auth_data=auth_data, nav_columns=nav_columns,message='Successful Insert')

        elif 'satButton' in request.form.keys():
            print(request.form)
            testscores = 400
            writing = request.form['writingScore']
            mathCalculator = request.form['mathCalcScore']
            math = request.form['mathScore']
            reading = request.form['readingScore']
            satComp = request.form['satCompScore']
            satType = request.form['satType']
            satTestDate =request.form['satTestDate']
            db.create_mock(mockType='sat',
                           mockInfo={'studentIDFK': studentID, 'writingScore': writing, 'writingMax': writing,
                                     'mathCalcScore': mathCalculator, 'mathCalcMax': testscores, 'mathScore': math,
                                     'mathMax': testscores, 'readingScore': reading, 'readingMax': testscores,
                                     'satCompScore': satComp, 'satType': satType, 'satTestDate': satTestDate})
            return render_template('/elements/mock_exam_form.html', auth_data=auth_data, nav_columns=nav_columns,message='Successful Insert')
        elif 'hsptButton' in request.form.keys():
            print(request.form)
            testScores = 200
            verbal = request.form['verbalScore']
            quantitativeMath = request.form['quantitativeScore']
            reading = request.form['readingScore']
            math = request.form['mathScore']
            language = request.form['languageScore']
            hsptComp = request.form['hsptCompScore']
            hsptType = request.form['hsptType']
            hsptTestDate = request.form['hsptTestDate']
            db.create_mock(mockType='hspt',
                           mockInfo={'studentIDFK': studentID, 'verbalScore': verbal, 'verbalMax': testScores,
                                     'quantitativeScore': quantitativeMath, 'readingScore': reading, 'readingMax': testScores,
                                     'mathScore':math,'mathMax': testScores, 'languageScore': language, 'languageMax': testScores,
                                     'hsptCompScore': hsptComp, 'hsptType': hsptType, 'satTestDate': hsptTestDate})
            return render_template('/elements/mock_exam_form.html', auth_data=auth_data, nav_columns=nav_columns,message='Successful Insert')
        elif 'iseeButton' in request.form.keys():
            print(request.form)
            testScores = 235
            verbal = request.form['verbalScore']
            quantitativeMath = request.form['quantitativeScore']
            reading = request.form['readingScore']
            math = request.form['mathScore']
            iseeComp = request.form['iseeCompScore']
            iseeType = request.form['iseeType']
            iseeTestDate = request.form['iseeTestDate']
            db.create_mock(mockType='isee',
                           mockInfo={'studentIDFK': studentID, 'verbalScore': verbal, 'verbalMax': testScores,
                                     'quantitativeScore': quantitativeMath, 'quantitativeMax': testScores,
                                     'readingScore': reading,'readingMax': testScores,'mathScore':math, 'mathMax': testScores,
                                     'iseeCompScore': iseeComp, 'iseeType': iseeType, 'iseeTestDate': iseeTestDate})
            return render_template('/elements/mock_exam_form.html', auth_data=auth_data, nav_columns=nav_columns,message='Successful Insert')
        else:
            return render_template('/elements/mock_exam_form.html', auth_data=auth_data, nav_columns=nav_columns,message='Successful Insert')

        return render_template('/elements/mock_exam_form.html', auth_data=auth_data, nav_columns=nav_columns)

@app.route("/testprep/update/<examType>/<examID>", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def testprep_update(examType, examID, auth_data=None):
    if request.method == 'GET':
        return render_template('/elements/mock_exam_form.html', auth_data=auth_data, nav_columns=nav_columns)
    if request.method == 'POST':
        update = db.update_mock(examType, examID)
        return render_template('error.html')
    return render_template('/test_prep_dashboard.html', auth_data=auth_data, nav_columns=nav_columns,message='Error while deleting')

@app.route("/testprep/delete/<examType>/<examID>", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def testprep_delete(examType, examID,auth_data = None):
    if request.method == 'GET':
        db.delete_mock(examType,examID)
        return render_template('/test_prep_dashboard.html', auth_data=auth_data, nav_columns=nav_columns, message='Successful Delete')
    return render_template('/test_prep_dashboard.html', auth_data=auth_data, nav_columns=nav_columns, message='Error while deleting')
