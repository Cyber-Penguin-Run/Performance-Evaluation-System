from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
from __main__ import app, secure_site, db

class Programs():
    nav_columns = {'Overview':'programs_overview','College Workshop': 'programs_college_summer_workshop',
                   'Academic Coaching': 'programs_academic_coaching',
                   'College Coaching': 'programs_college_coaching', 'Education Future': 'programs_education_future',
                   'Executive Function': 'programs_exec_function',
                   'Executive Function Mini': 'programs_exec_function_mini',
                   'Small Groups': 'programs_small_groups', 'Study Spot': 'programs_study_spot',
                   'Program Test Prep': 'programs_test_prep'
                   }
