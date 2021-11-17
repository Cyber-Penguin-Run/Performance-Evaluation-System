import re
from flask import Flask, json, render_template, url_for, request, redirect, jsonify
from flask.helpers import make_response
from app import students
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
        

        else:
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
            familyID = db.create_family(request.form['familyName'])
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