from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
import uuid
from programs_dashboard import Programs
from __main__ import app, secure_site, db

nav_columns = {"Staff":"admin_staff", "Add Staff":"admin_staff",
              "Families":"admin_families", "Business":"admin_business","Programs":"programs_overview"}


@app.route("/admin/staff", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def admin_staff(auth_data = None):
    staff_table = db.get_like_users({"username":""})
    if request.method == 'GET':
        return render_template('staff.html',auth_data=auth_data, nav_columns= nav_columns, staff_table=staff_table)
    if request.method == "POST":
        if "deleteStaff" in request.form.keys():
            deleted = db.delete_staff(request.form.get("deleteStaff"))
            staff_table = db.get_like_users({"username":""})
            if deleted:
                return render_template('staff.html',auth_data=auth_data, nav_columns= nav_columns, message="Staff member deleted.", staff_table=staff_table)
            return render_template('staff.html',auth_data=auth_data, nav_columns= nav_columns, message="Staff was not deleted.", staff_table=staff_table)
        

@app.route("/admin/families", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def admin_families(auth_data = None):
    family_table = db.query('Select * FROM family')
    if request.method == 'GET':
        return render_template("family.html",auth_data=auth_data, nav_columns=nav_columns,family_table=family_table)

@app.route("/admin/business", methods = ["POST", "GET"])
@secure_site
def admin_business(auth_data = None):
    if request.method == 'GET':
        return render_template("/elements/family_form.html",auth_data=auth_data, nav_columns=nav_columns)
    elif request.method == 'POST':
        familyName = request.form['familyName']
        db.create_family(familyName)
        return render_template('layout.html'), {"Refresh": "2; url=/admin/families"}
    return render_template('/elements/family_form.html', auth_data=auth_data, nav_columns=nav_columns)




#skeleton function for admins to delete families
@app.route("/admin/families/update/<familyID>", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def admin_families_update(familyID,auth_data = None):
    if request.method == 'GET':
        family = db.query("SELECT * FROM family WHERE familyID = '%s'" % familyID)
        print(family[0])
        return render_template('/elements/family_form.html', auth_data=auth_data,
                               nav_columns=nav_columns, familyName=family[0]['familyName'])
    if request.method == 'POST':
        print('updated')
        family = db.query("SELECT * FROM family WHERE familyID = '%s'" % familyID)
        familyName = request.form.get('familyName')
        isupdated = db.edit_family(familyID, familyName)
        if isupdated:
            return render_template('family.html', auth_data=auth_data, nav_columns=nav_columns,
                                   message='updated successfully')
        else:
            return render_template('family.html', auth_data=auth_data, nav_columns=nav_columns,
                                   message='error while updating')



#skeleton function for admins to delete families
@app.route("/admin/families/delete/<familyID>", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def admin_families_delete(familyID,auth_data = None):
    if request.method == 'GET':
        family = db.query("SELECT * FROM family WHERE familyID = '%s'" % familyID)
        print(family[0])
        return render_template('/elements/family_form.html', auth_data=auth_data,
                               nav_columns=nav_columns, familyName=family[0]['familyName'])



@app.route("/programs/overview", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def programs_overview(auth_data = None):
    if request.method == 'GET':
        getPrograms = db.query("SELECT * FROM studentPrograms")
        return render_template('studentPrograms.html',auth_data=auth_data, nav_columns=Programs.nav_columns, getPrograms=getPrograms)
    if request.method == 'POST':
        pass

@app.route("/programs/create/", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def programs_create(programID = None,auth_data = None):
    if request.method == 'GET':
        getPrograms = db.query("SELECT * FROM studentPrograms")
        return render_template('/elements/programs_form.html',auth_data=auth_data, nav_columns=Programs.nav_columns,
                               programID=programID, getPrograms=getPrograms)
    if request.method == 'POST':
        if 'SummerButton' in request.form.keys():
            print(request.form)
            start = request.form['SummerStart']
            end = request.form['SummerEnd']
            if request.form['TestTakenYes']:
                testTaken = 1
            elif request.form['TestTakenNo']:
                testTaken = 0
            gpa = request.form['GPA']
            notes = request.form['Notes']
            if Programs.create_program(programType='SummerWorkshop',programInfo={'fromDate':start,'endDate':end,
                                                                                 'testTaken':testTaken,'gpa':gpa,
                                                                                 'notes':notes,'programIDFK':programID
                                                                                 }):
                return render_template('/programs/programs_form.html',auth_data=auth_data,nav_columns=Programs.nav_columns,message='successful insert')
        if 'academicCoachButton' in request.form.keys():
            print(request.form)
            hours = request.form['hoursWeek']
            notes = request.form['Notes']
            concernArea = request.form['concernArea']
            english = request.form['englishGrade']
            history = request.form['historyGrade']
            math = request.form['mathGrade']
            science = request.form['scienceGrade']
            foreignLanguage = request.form['foreignLanguageGrade']
            if Programs.create_program(programType='AcademicCoaching',programInfo={'programIDFK':programID,'hoursWeek':hours,
                                                                                   'notes':notes, 'concernArea':concernArea,
                                                                                   'englishGrade':english,'historyGrade':history,
                                                                                   'mathGrade':math,'scienceGrade':science,
                                                                                   'foreignLanguageGrade':foreignLanguage}):
                return render_template('/programs/programs_form.html',auth_data=auth_data,nav_columns=Programs.nav_columns,message='successful insert')

        if 'collegeCoachButton' in request.form.keys():
            print(request.form)
            hours = request.form['hoursWeek']
            notes = request.form['Notes']
            concernArea = request.form['concernArea']
            english = request.form['englishGrade']
            history = request.form['historyGrade']
            math = request.form['mathGrade']
            science = request.form['scienceGrade']
            foreignLanguage = request.form['foreignLanguageGrade']
            if Programs.create_program(programType='CollegeCoaching',programInfo={'programIDFK':programID,'hoursWeek':hours,
                                                                                   'notes':notes, 'concernArea':concernArea,
                                                                                   'englishGrade':english,'historyGrade':history,
                                                                                   'mathGrade':math,'scienceGrade':science,
                                                                                   'foreignLanguageGrade':foreignLanguage}):
                return render_template('/programs/programs_form.html',auth_data=auth_data,nav_columns=Programs.nav_columns,message='successful insert')


@app.route('/programs/CollegeSummerWorkshop', methods=['GET', 'POST', 'PUT', 'DELETE'])
@secure_site
def programs_college_summer_workshop(auth_data=None):
    if request.method == 'GET':
        getPrograms = db.query("SELECT * FROM programCollegeSummerWorkshop")
        return render_template('/programs/SummerWorkshop.html', auth_data=auth_data, nav_columns=Programs.nav_columns,
                               getPrograms=getPrograms)
    if request.method == 'POST':
        pass

@app.route('/programs/Academic_Coaching', methods=['GET', 'POST', 'PUT', 'DELETE'])
@secure_site
def programs_academic_coaching(auth_data=None):
    if request.method == 'GET':
        getPrograms = db.query("SELECT * FROM programAcademicCoaching")
        return render_template('/programs/AcademicCoaching.html', auth_data=auth_data, nav_columns=Programs.nav_columns,
                               getPrograms=getPrograms)
    if request.method == 'POST':
        pass

@app.route('/programs/College_Coaching', methods=['GET', 'POST', 'PUT', 'DELETE'])
@secure_site
def programs_college_coaching(auth_data=None):
    if request.method == 'GET':
        getPrograms = db.query("SELECT * FROM programCollegeCoaching")
        return render_template('/programs/CollegeCoaching.html', auth_data=auth_data, nav_columns=Programs.nav_columns,
                               getPrograms=getPrograms)
    if request.method == 'POST':
        pass

@app.route('/programs/Education_Future', methods=['GET', 'POST', 'PUT', 'DELETE'])
@secure_site
def programs_education_future(auth_data=None):
    if request.method == 'GET':
        getPrograms = db.query("SELECT * FROM programEducationFuture")
        return render_template('/programs/EducationFuture.html', auth_data=auth_data, nav_columns=Programs.nav_columns,
                               getPrograms=getPrograms)
    if request.method == 'POST':
        pass

@app.route('/programs/Exec_Function', methods=['GET', 'POST', 'PUT', 'DELETE'])
@secure_site
def programs_exec_function(auth_data=None):
    if request.method == 'GET':
        getPrograms = db.query("SELECT * FROM programExecFunction")
        return render_template('/programs/ExecutiveFunction.html', auth_data=auth_data, nav_columns=Programs.nav_columns,
                               getPrograms=getPrograms)
    if request.method == 'POST':
        pass

@app.route('/programs/Exec_Function_Mini', methods=['GET', 'POST', 'PUT', 'DELETE'])
@secure_site
def programs_exec_function_mini(auth_data=None):
    if request.method == 'GET':
        getPrograms = db.query("SELECT * FROM programExecFunctionMini")
        return render_template('/programs/ExecutiveFunctionMini.html', auth_data=auth_data, nav_columns=Programs.nav_columns,
                               getPrograms=getPrograms)
    if request.method == 'POST':
        pass

@app.route('/programs/Small_Groups', methods=['GET', 'POST', 'PUT', 'DELETE'])
@secure_site
def programs_small_groups(auth_data=None):
    if request.method == 'GET':
        getPrograms = db.query("SELECT * FROM programSmallGroups")
        return render_template('/programs/SmallGroups.html', auth_data=auth_data, nav_columns=Programs.nav_columns,
                               getPrograms=getPrograms)
    if request.method == 'POST':
        pass

@app.route('/programs/Study_Spot', methods=['GET', 'POST', 'PUT', 'DELETE'])
@secure_site
def programs_study_spot(auth_data=None):
    if request.method == 'GET':
        getPrograms = db.query("SELECT * FROM programStudySpot")
        return render_template('/programs/StudySpot.html', auth_data=auth_data, nav_columns=Programs.nav_columns,
                               getPrograms=getPrograms)
    if request.method == 'POST':
        pass

@app.route('/programs/Test_Prep', methods=['GET', 'POST', 'PUT', 'DELETE'])
@secure_site
def programs_test_prep(auth_data=None):
    if request.method == 'GET':
        getPrograms = db.query("SELECT * FROM programTestPrep")
        return render_template('/programs/TestPrep.html', auth_data=auth_data, nav_columns=Programs.nav_columns,
                               getPrograms=getPrograms)
    if request.method == 'POST':
        pass