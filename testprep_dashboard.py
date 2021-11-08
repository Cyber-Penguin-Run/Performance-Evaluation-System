from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
from __main__ import app, secure_site, db

@app.route("/testprep", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def testprep(auth_data = None):
    return "/testprep"