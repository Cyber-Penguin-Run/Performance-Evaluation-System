from flask.helpers import make_response
from datetime import datetime, timedelta
from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
from __main__ import app, secure_site, db


@app.route("/api/families", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def api_families(auth_data = None):
    if request.method == "GET":

        families = db.get_like_families()

        return jsonify(families)


@app.route("/api/coach/students", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def api_coach_students(auth_data = None):
    if request.method == "GET":
        students = db.get_coach_students(auth_data['user_id'])

        return jsonify(students)

@app.route("/api/admin/staff", methods = ["POST", "GET", "PUT", "DELETE"])
def api_admin_staff(auth_data = None):
    if request.method == "GET":
        staff_data = request.json

        results = db.get_like_staff(staff_data)

        return jsonify(results)


        


