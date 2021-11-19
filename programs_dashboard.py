import uuid
from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
from app import app, secure_site, db

class Programs():
    nav_columns = {'Overview':'programs_overview','Students':'programs_students',
                   'College Workshop': 'programs_college_summer_workshop',
                   'Academic Coaching': 'programs_academic_coaching',
                   'College Coaching': 'programs_college_coaching', 'Education Future': 'programs_education_future',
                   'Executive Function': 'programs_exec_function',
                   'Executive Function Mini': 'programs_exec_function_mini',
                   'Small Groups': 'programs_small_groups', 'Study Spot': 'programs_study_spot',
                   'Program Test Prep': 'programs_test_prep'
                   }
    def create_program(self,programType, programInfo):
        programID = uuid.uuid4().hex
        programInfo['programID']=programID
        try:
            db.cursor.execute('INSERT INTO studentPrograms(programID, studentIDFK, programType) values (?,?,?)',(programID,programInfo['studentID'],programType))
        except Exception as e:
            print(e)
            return e
        if programType =='SummerWorkshop':
            program_insert = """INSERT INTO programCollegeSummerWorkshop(fromDate,endDate,testTaken,gpa,notes,programIDFK)
            values ('%(fromDate)s','%(endDate)s','%(testTaken)s','%(notes)s','%(programID)s')""" % programInfo

        if programType =='AcademicCoaching':
            program_insert = """INSERT INTO programAcademicCoaching(programIDFK,hoursWeek,notes,concernArea,englishGrade,
            historyGrade,mathGrade,scienceGrade,foreignLanguageGrade) 
            values ('%(programID)s','%(hours)s','%(notes)s','%(concernArea)s','%(english)s', '%(history)s', '%(math)s',
            '%(science)s','%(foreignLanguage)s'
            )""" % programInfo

        if programType =='CollegeCoaching':
            program_insert = """INSERT INTO programCollegeCoaching(programIDFK,froom,Enddate,Testtaken,GPA,Notes) 
            values ('%(programID)s','%(fromDate)s','%(endDate)s','%(testTaken)s','%(notes)s')""" % programInfo

        if programType =='EducationFuture':
            program_insert = """INSERT INTO programCollegeCoaching(programIDFK,hoursWeek,areaInterest,notes) 
            values ('%(programID)s','%(hours)s','%(concern)s','%(notes)s')""" % programInfo

        if programType =='ExecutiveFunction':
            program_insert = """INSERT INTO programExecFunction(programIDFK,hoursWeek,notes,concernArea,englishGrade,
                        historyGrade,mathGrade,scienceGrade,foreignLanguageGrade) 
                        values ('%(programID)s','%(hoursWeek)s','%(notes)s','%(concernArea)s','%(english)s', '%(history)s', '%(math)s',
                        '%(science)s','%(foreignLanguage)s'
                        )""" % programInfo

        if programType =='ExecutiveFunctionMini':
            program_insert = """INSERT INTO programAcademicCoaching(programIDFK,hoursWeek,notes,concernArea,englishGrade,
                        historyGrade,mathGrade,scienceGrade,foreignLanguageGrade) 
                        values ('%(programID)s','%(hoursWeek)s','%(notes)s','%(concernArea)s','%(english)s', '%(history)s', '%(math)s',
                        '%(science)s','%(foreignLanguage)s'
                        )""" % programInfo

        if programType =='smallGroups':
            program_insert = """INSERT INTO programAcademicCoaching(programIDFK,hoursWeek,notes,concernArea,englishGrade,
                        historyGrade,mathGrade,scienceGrade,foreignLanguageGrade) 
                        values ('%(programID)s','%(hoursWeek)s','%(notes)s','%(concernArea)s','%(english)s', '%(history)s', '%(math)s',
                        '%(science)s','%(foreignLanguage)s'
                        )""" % programInfo

        if programType =='studySpot':
            program_insert = """INSERT INTO programAcademicCoaching(programIDFK,hoursWeek,notes,concernArea,englishGrade,
                        historyGrade,mathGrade,scienceGrade,foreignLanguageGrade) 
                        values ('%(programID)s','%(hoursWeek)s','%(notes)s','%(concernArea)s','%(english)s', '%(history)s', '%(math)s',
                        '%(science)s','%(foreignLanguage)s'
                        )""" % programInfo

        if programType =='testPrep':
            program_insert = """INSERT INTO programAcademicCoaching(programIDFK,testdate,Testtype,prevtaken,prevcourse,
                        Testaccomidations,Matheval,Scienceevl,Englisheval,Histeval) 
                        values ('%(programID)s','%(hoursWeek)s','%(notes)s','%(concernArea)s','%(english)s', '%(history)s', '%(math)s',
                        '%(science)s','%(foreignLanguage)s'
                        )""" % programInfo

        try:
            print("executing program query")
            print(program_insert)
            db.cursor.execute(program_insert)
            db.cursor.commit()
            return True
        except Exception as e:
            print('error during insertion of program', e)
            return False