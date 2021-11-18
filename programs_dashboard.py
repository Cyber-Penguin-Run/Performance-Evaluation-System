from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
from __main__ import app, secure_site, db

class Programs():
    nav_columns = {'Overview':'programs_overview','Create Program':'programs_create','College Workshop': 'programs_college_summer_workshop',
                   'Academic Coaching': 'programs_academic_coaching',
                   'College Coaching': 'programs_college_coaching', 'Education Future': 'programs_education_future',
                   'Executive Function': 'programs_exec_function',
                   'Executive Function Mini': 'programs_exec_function_mini',
                   'Small Groups': 'programs_small_groups', 'Study Spot': 'programs_study_spot',
                   'Program Test Prep': 'programs_test_prep'
                   }
    def create_program(self,programType, programInfo):
        if programType =='SummerWorkshop':
            program_insert = """INSERT INTO programCollegeSummerWorkshop(fromDate,endDate,testTaken,gpa,notes,programIDFK)
            values ('%(fromDate)s','%(endDate)s','%(testTaken)s','%(notes)s','%(programIDFK)s')"""

        if programType =='AcademicCoaching':
            program_insert = """INSERT INTO programAcademicCoaching(programIDFK,hoursWeek,notes,concernArea,englishGrade,
            historyGrade,mathGrade,scienceGrade,foreignLanguageGrade) 
            values ('%(programID)s','%(hours)s','%(notes)s','%(concernArea)s','%(english)s', '%(english)s', '%(english)s',
            )"""

        try:
            print("executing program query")
            print(program_insert)
            self.cursor.execute(program_insert)
            self.cursor.commit()
            return True
        except Exception as e:
            print('error during insertion of program', e)
            return False