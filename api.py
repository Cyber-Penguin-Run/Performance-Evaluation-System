from flask.helpers import make_response
from datetime import datetime, timedelta
from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
from __main__ import app, secure_site, db


@app.route("/api/family", methods = ["POST", "GET", "PUT", "DELETE"])
#@secure_site
def familyroute(auth_data = None):
    if request.method == "GET":
        families = db.get_like_families()

        return jsonify(families)
