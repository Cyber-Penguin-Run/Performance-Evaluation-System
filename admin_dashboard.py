from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from connection import Database
import uuid
from __main__ import app, secure_site, db

nav_columns = {"Overview":"admin_overview", "Staff":"admin_staff", "Add Staff":"admin_staff_change",
              "Families":"admin_families", "Business":"admin_business","Programs":"programs_overview"}


@app.route("/admin/overview", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def admin_overview(auth_data = None):
    users_table = db.query('Select * FROM users')
    return render_template('admin.html',auth_data=auth_data, nav_columns= nav_columns, users_table=users_table)

@app.route("/admin/staff", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def admin_staff(auth_data = None):
    staff_table = db.query('Select * FROM staff')
    if request.method == 'GET':
        return render_template('staff.html',auth_data=auth_data, nav_columns= nav_columns, staff_table=staff_table)
    elif request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        phoneNumber = request.form['phoneNumber']
        email = request.form['email']
        staff_insert = db.query('INSERT INTO staff(firstName, lastName, phoneNumber, email) Values (%s,%s,%s,%s)',
                                (firstName, lastName, phoneNumber, email))
        # db.cursor.execute(family_insert)
        return render_template('success.html'), {"Refresh": "2; url=/admin/families"}

    return render_template('admin.html', auth_data=auth_data, nav_columns=nav_columns)

@app.route("/admin/staff/change", methods = ["POST", "GET", "PUT", "DELETE"])
@secure_site
def admin_staff_change(auth_data = None):
    if request.method == 'GET':
        staff_table = db.query('Select * FROM staff')
        return render_template('/elements/staff_form.html',auth_data=auth_data,nav_columns=nav_columns,staff_table=staff_table)
    if request.method == 'POST':
        pass

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