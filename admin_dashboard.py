from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
from programs_dashboard import Programs
from __main__ import app, secure_site, db


nav_columns = {"Staff":"admin_staff", "Families":"admin_families", "Business":"admin_business","Programs":"programs_overview"}
programs = Programs()

@app.route("/admin/staff", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def admin_staff(auth_data = None):
    staff_table = db.get_like_users({"username":""})
    if request.method == 'GET':
        return render_template('staff.html',auth_data=auth_data, nav_columns= nav_columns, staff_table=staff_table)
    if request.method == "POST":
        print(request.form)
        if "searchBtn" in request.form.keys():
            print("searching")
            staff_table = db.get_staff_fullname(request.form.get("fullname"))
            return render_template('staff.html',auth_data=auth_data, nav_columns= nav_columns, staff_table=staff_table)

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

    if request.method == "POST":

        if "searchBtn" in request.form.keys():
            print("searching")
            family_table = db.get_families_fullname(request.form.get("fullname"))
            return render_template('family.html',auth_data=auth_data, nav_columns=nav_columns, family_table=family_table)

        if "deleteFamily" in request.form.keys():
            deleted = db.delete_family(request.form.get("deleteFamily"))
            family_table = db.query('Select * FROM family')
            if deleted:
                return render_template('family.html', auth_data=auth_data, nav_columns=nav_columns, family_table=family_table,
                                    message='family deleted successfully.')
            else:
                return render_template('family.html', auth_data=auth_data, nav_columns=nav_columns, family_table=family_table,
                                    message='Error trying to delete family.')



#skeleton function for admins to delete families
@app.route("/admin/families/update/<familyID>", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def admin_families_update(familyID, auth_data = None):
    if request.method == 'GET':
        family = db.get_family(familyID)
        states = db.getStates()
        return render_template('/elements/family_form.html', auth_data=auth_data,
                               nav_columns=nav_columns, family=family, states=states)
    if request.method == 'POST':
        print(request.form)
        option = request.form.get("submitBtn")

        if option == "createStudent":
            student_family = request.form.get("familyID")
            student_firstname = request.form.get("studentFirstname")
            student_lastname = request.form.get("studentLastname")
            student_school = request.form.get("studentSchool")

            if db.create_student({"firstName":student_firstname, "lastName":student_lastname, "school":student_school, "familyIDFK":student_family}):
                family = db.get_family(familyID)
                states = db.getStates()
                return render_template('/elements/family_form.html', auth_data=auth_data,
                                    nav_columns=nav_columns, family=family, states=states)

        if option == "deleteStudent":
            if db.delete_student(request.form.get("studentID")):
                family = db.get_family(familyID)
                states = db.getStates()
                return render_template('/elements/family_form.html', auth_data=auth_data,
                                    nav_columns=nav_columns, family=family, states=states)

        if option == "deleteParent":
            if db.delete_parent(request.form.get("parentID")):
                family = db.get_family(familyID)
                states = db.getStates()
                return render_template('/elements/family_form.html', auth_data=auth_data,
                                    nav_columns=nav_columns, family=family, states=states)


        if option == "createParent":
            try:
                username = request.form['username']
                username = username.lower()
                password = request.form['password']
                address = request.form['address']
                state = request.form['state']
                firstname = request.form['firstname']
                lastname = request.form['lastname']
                phone = request.form['phoneNumber']
                email = request.form['emailAddress']
                user_role = "parent"
            except KeyError as e:
                print("Missing arguments for register.")
                return render_template('error.html'), {"Refresh": "4; url=/register"}

            new_user = {"username": username, "userPassword": password, "userAddress": address, "stateIDFK": state,
                        "firstName": firstname, "lastName": lastname, "phoneNumber": phone.strip(), "email": email,
                        "userRole": user_role}

            if user_role == "parent":
                family = request.form.get("familyID")
                new_user['familyID'] = family

            if db.create_user(new_user):
                    family = db.get_family(familyID)
                    states = db.getStates()
                    return render_template('/elements/family_form.html', auth_data=auth_data,
                                        nav_columns=nav_columns, family=family, states=states)
        

        if option == "updateFamily":
            family = db.query("SELECT * FROM family WHERE familyID = '%s'" % familyID)
            familyName = request.form.get('familyName')
            familyStatus = request.form.get('familyStatus')
            isupdated = db.edit_family(familyID, familyName, familyStatus)
            if isupdated:
                return redirect(url_for("admin_families", auth_data=auth_data))
            else:
                return redirect(url_for("admin_families", auth_data=auth_data))




@app.route("/admin/families/add", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def admin_families_add(auth_data = None):
    if request.method == 'GET':
        family = db.get_family("")
        states = db.getStates()
        return render_template('/elements/family_form.html', auth_data=auth_data,
                               nav_columns=nav_columns, family=family, states=states)

    if request.method == "POST":
        option = request.form.get("submitBtn")

        if option == "createFamily":
            familyID = db.create_family(request.form['familyName'], request.form['familyStatus'])
            if familyID:
                family = db.get_family(familyID)
                states = db.getStates()
                return render_template('/elements/family_form.html', auth_data=auth_data,
                                    nav_columns=nav_columns, family=family, states=states)


        print(option)
        family = db.get_family("")
        states = db.getStates()
        return render_template('/elements/family_form.html', auth_data=auth_data,
                               nav_columns=nav_columns, family=family, states=states)





@app.route("/admin/business", methods = ["POST", "GET"])
@secure_site
def admin_business(auth_data = None):
    family_table = db.query('Select * FROM family ORDER BY familyStatus')
    if request.method == 'GET':
        return render_template("family.html",auth_data=auth_data, nav_columns=nav_columns,family_table=family_table)



@app.route("/programs/overview", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def programs_overview(auth_data = None):
    if request.method == 'GET':
        getPrograms = db.query("SELECT * FROM studentPrograms left JOIN student on studentPrograms.studentIDFK=student.studentID")
        return render_template('studentPrograms.html',auth_data=auth_data, nav_columns=Programs.nav_columns, getPrograms=getPrograms)
    if request.method == 'POST':
        pass

@app.route("/programs/students", methods=["GET","POST"])
@secure_site
def programs_students(auth_data = None):
    if request.method == "GET":
        if auth_data['userPerms']['adminDashboard']:
            students = db.query("SELECT * FROM student")
        else:
            students = db.get_coach_students(auth_data['user_id'])
        return render_template("/programs/programStudents.html", auth_data=auth_data, nav_columns=Programs.nav_columns,
                               students=students)

    if request.method == "POST":
        fullname = request.form.get("fullname")

        students = db.get_students_fullname(fullname)

        return render_template("/programs/programStudents.html", auth_data=auth_data, nav_columns=Programs.nav_columns,
                               students=students)

@app.route("/programs/create/<studentID>", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def programs_create(studentID,auth_data = None):
    if request.method == 'GET':
        getPrograms = db.query("SELECT * FROM studentPrograms")
        return render_template('/elements/programs_form.html',auth_data=auth_data, nav_columns=Programs.nav_columns,
                               studentID=studentID, getPrograms=getPrograms)
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
            if programs.create_program(programType='SummerWorkshop',programInfo={'fromDate':start,'endDate':end,
                                                                                 'testTaken':testTaken,'gpa':gpa,
                                                                                 'notes':notes,'studentID':studentID
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
            if programs.create_program(programType='AcademicCoaching',programInfo={'studentID':studentID,'hoursWeek':hours,
                                                                                   'notes':notes, 'concernArea':concernArea,
                                                                                   'english':english,'history':history,
                                                                                   'mathGrade':math,'scienceGrade':science,
                                                                                   'foreignLanguageGrade':foreignLanguage}):
                return render_template('/programs/programs_form.html',auth_data=auth_data,nav_columns=Programs.nav_columns,message='successful insert')

        if 'collegeCoachButton' in request.form.keys():
            print(request.form)
            start = request.form['FromDate']
            end = request.form['EndDate']
            if request.form['TestTakenYes']:
                testTaken = 1
            elif request.form['TestTakenNo']:
                testTaken = 0
            gpa = request.form['GPA']
            notes = request.form['Notes']
            if programs.create_program(programType='CollegeCoaching',programInfo={'fromDate':start,'endDate':end,
                                                                                 'testTaken':testTaken,'gpa':gpa,
                                                                                 'notes':notes,'studentID':studentID
                                                                                 }):
                return render_template('/programs/programs_form.html',auth_data=auth_data,nav_columns=Programs.nav_columns,message='successful insert')
        if 'EducationFutureButton' in request.form.keys():
            print(request.form)
            hours = request.form['hoursWeek']
            concern = request.form['concernArea']
            notes = request.form['Notes']
            if programs.create_program(programType='EducationFuture', programInfo={'hoursWeek':hours, 'areaInterest':concern,
                                                                                   'notes':notes, 'studentID':studentID}):
                return render_template('/programs/programs_form.html',auth_data=auth_data,
                                       nav_columns=Programs.nav_columns,message='successful insert')

        if 'execFunctionButton' in request.form.keys():
            print(request.form)
            hours = request.form['hoursWeek']
            notes = request.form['Notes']
            concernArea = request.form['concernArea']
            english = request.form['englishGrade']
            history = request.form['historyGrade']
            math = request.form['mathGrade']
            science = request.form['scienceGrade']
            foreignLanguage = request.form['foreignLanguageGrade']
            if programs.create_program(programType='ExecutiveFunction',
                                       programInfo={'studentID':studentID,'hoursWeek':hours,
                                                    'notes':notes, 'concernArea':concernArea,
                                                    'english':english,'history':history,
                                                    'math':math,'science':science,
                                                    'foreignLanguage':foreignLanguage}):
                return render_template('/elements/programs_form.html',auth_data=auth_data,
                                       nav_columns=Programs.nav_columns,message='successful insert')

        if 'execFunctionMiniButton' in request.form.keys():
            print(request.form)
            hours = request.form['hoursWeek']
            notes = request.form['Notes']
            concernArea = request.form['concernArea']
            english = request.form['englishGrade']
            history = request.form['historyGrade']
            math = request.form['mathGrade']
            science = request.form['scienceGrade']
            foreignLanguage = request.form['foreignLanguageGrade']
            if programs.create_program(programType='ExecutiveFunctionMini',
                                       programInfo={'studentID':studentID, 'hoursWeek': hours,
                                                    'notes': notes, 'concernArea': concernArea,
                                                    'english': english, 'history': history,
                                                    'math': math, 'science': science,
                                                    'foreignLanguage': foreignLanguage}):
                return render_template('/elements/programs_form.html', auth_data=auth_data,
                                       nav_columns=Programs.nav_columns, message='successful insert')

        if 'smallGroupsButton' in request.form.keys():
            hours = request.form['hoursWeek']
            notes = request.form['Notes']
            concernArea = request.form['concernArea']
            english = request.form['englishGrade']
            history = request.form['historyGrade']
            math = request.form['mathGrade']
            science = request.form['scienceGrade']
            foreignLanguage = request.form['foreignLanguageGrade']
            if programs.create_program(programType='smallGroups',
                                       programInfo={'studentID':studentID, 'hoursWeek': hours,
                                                    'notes': notes, 'concernArea': concernArea,
                                                    'english': english, 'history': history,
                                                    'mathGrade': math, 'scienceGrade': science,
                                                    'foreignLanguageGrade': foreignLanguage}):
                return render_template('/elements/programs_form.html', auth_data=auth_data,
                                       nav_columns=Programs.nav_columns, message='successful insert')

        if 'studySpotButton' in request.form.keys():
            hours = request.form['hoursWeek']
            notes = request.form['Notes']
            concernArea = request.form['concernArea']
            english = request.form['englishGrade']
            history = request.form['historyGrade']
            math = request.form['mathGrade']
            science = request.form['scienceGrade']
            foreignLanguage = request.form['foreignLanguageGrade']
            if programs.create_program(programType='studySpot',
                                       programInfo={'studentID':studentID, 'hoursWeek': hours,
                                                    'notes': notes, 'concernArea': concernArea,
                                                    'english': english, 'history': history,
                                                    'mathGrade': math, 'scienceGrade': science,
                                                    'foreignLanguageGrade': foreignLanguage}):
                return render_template('/elements/programs_form.html', auth_data=auth_data,
                                       nav_columns=Programs.nav_columns, message='successful insert')

        if 'testPrepButton' in request.form.keys():
            date = request.form['testDate']
            type = request.form['Testtype']
            if request.form['TestTakenYes']:
                testTaken = 1
            elif request.form['TestTakenNo']:
                testTaken = 0
            if request.form['PrevCourseYes']:
                courseTaken = 1
            elif request.form['PrevCourseNo']:
                courseTaken = 0
            if request.form['accommodationsYes']:
                accommodations = 1
            elif request.form['accommodationsNo']:
                accommodations = 0
            math = request.form['Matheval']
            science = request.form['Scienceevl']
            english = request.form['Englisheval']
            history = request.form['Histeval']
            if programs.create_program(programType='testPrep',
                                       programInfo={'testdate': date,
                                           'Testtype': type, 'prevtaken': testTaken,'prevcourse': courseTaken,
                                           'Testaccomidations': accommodations, 'Matheval':math,'Scienceeval':science,
                                           'Englisheval':english,'Histeval':history, 'studentID':studentID}):
                return render_template('/elements/programs_form.html', auth_data=auth_data,
                                       nav_columns=Programs.nav_columns, message='successful insert')

@app.route('/programs/CollegeSummerWorkshop', methods=['GET'])
@secure_site
def programs_college_summer_workshop(auth_data=None):
    if request.method == 'GET':
        getPrograms = db.query("SELECT * FROM programCollegeSummerWorkshop")
        return render_template('/programs/SummerWorkshop.html', auth_data=auth_data, nav_columns=Programs.nav_columns,
                               getPrograms=getPrograms)

@app.route('/programs/Academic_Coaching', methods=['GET'])
@secure_site
def programs_academic_coaching(auth_data=None):
    if request.method == 'GET':
        getPrograms = db.query("SELECT * FROM programAcademicCoaching")
        return render_template('/programs/AcademicCoaching.html', auth_data=auth_data, nav_columns=Programs.nav_columns,
                               getPrograms=getPrograms)

@app.route('/programs/College_Coaching', methods=['GET'])
@secure_site
def programs_college_coaching(auth_data=None):
    if request.method == 'GET':
        getPrograms = db.query("SELECT * FROM programCollegeCoaching")
        return render_template('/programs/CollegeCoaching.html', auth_data=auth_data, nav_columns=Programs.nav_columns,
                               getPrograms=getPrograms)

@app.route('/programs/Education_Future', methods=['GET'])
@secure_site
def programs_education_future(auth_data=None):
    if request.method == 'GET':
        getPrograms = db.query("SELECT * FROM programEducationFuture")
        return render_template('/programs/EducationFuture.html', auth_data=auth_data, nav_columns=Programs.nav_columns,
                               getPrograms=getPrograms)

@app.route('/programs/Exec_Function', methods=['GET'])
@secure_site
def programs_exec_function(auth_data=None):
    if request.method == 'GET':
        getPrograms = db.query("SELECT * FROM programExecFunction")
        return render_template('/programs/ExecutiveFunction.html', auth_data=auth_data, nav_columns=Programs.nav_columns,
                               getPrograms=getPrograms)

@app.route('/programs/Exec_Function_Mini', methods=['GET'])
@secure_site
def programs_exec_function_mini(auth_data=None):
    if request.method == 'GET':
        getPrograms = db.query("SELECT * FROM programExecFunctionMini")
        return render_template('/programs/ExecutiveFunctionMini.html', auth_data=auth_data, nav_columns=Programs.nav_columns,
                               getPrograms=getPrograms)

@app.route('/programs/Small_Groups', methods=['GET'])
@secure_site
def programs_small_groups(auth_data=None):
    if request.method == 'GET':
        getPrograms = db.query("SELECT * FROM programSmallGroups")
        return render_template('/programs/SmallGroups.html', auth_data=auth_data, nav_columns=Programs.nav_columns,
                               getPrograms=getPrograms)

@app.route('/programs/Study_Spot', methods=['GET'])
@secure_site
def programs_study_spot(auth_data=None):
    if request.method == 'GET':
        getPrograms = db.query("SELECT * FROM programStudySpot")
        return render_template('/programs/StudySpot.html', auth_data=auth_data, nav_columns=Programs.nav_columns,
                               getPrograms=getPrograms)

@app.route('/programs/Test_Prep', methods=['GET'])
@secure_site
def programs_test_prep(auth_data=None):
    if request.method == 'GET':
        getPrograms = db.query("SELECT * FROM programTestPrep")
        return render_template('/programs/TestPrep.html', auth_data=auth_data, nav_columns=Programs.nav_columns,
                               getPrograms=getPrograms)