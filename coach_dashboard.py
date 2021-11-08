from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
from __main__ import app, secure_site, db

@app.route("/coach/home", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def coach_home(auth_data = None):
    return "/coach/home"

@app.route("/coach/info", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def coach_info(auth_data = None):
    return "/coach/info"