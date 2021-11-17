from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
import uuid
from __main__ import app, secure_site, db


nav_columns = {"Staff":"admin_staff", "Families":"admin_families", "Business":"admin_business"}


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
def admin_families_update(familyID, auth_data = None):
    if request.method == 'GET':
        family = db.get_family(familyID)
        states = db.getStates()
        return render_template('/elements/family_form.html', auth_data=auth_data,
                               nav_columns=nav_columns, family=family, states=states)
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