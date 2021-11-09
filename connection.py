from flask.json import JSONEncoder, jsonify
import pyodbc
import random
import json
import uuid

class Database:
    def __init__(self):
        server = 'CoT-CIS3365-10.cougarnet.uh.edu'
        #server = "DESKTOP-MCGVN84\SQLEXPRESS"
        database = 'Enrichery'
        username = 'Test'
        password = 'P@ssw0rd1'

        try:
            self.cnx = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
            self.cursor = self.cnx.cursor()
        except Exception as e:
            print("Error while connecting to database:")
            print(e)
        else:
            print("Connection to database successful.")

    def results_as_dict(self):
        return [dict(zip([column[0] for column in self.cursor.description], row))
             for row in self.cursor.fetchall()]

    def create_family(self, familyName):
        familyID = uuid.uuid4().hex
        print(familyID)
        if familyName is not None:
            family_insert = ("INSERT INTO family(familyID, familyName)"
                                       "Values (?,?)")
            values = (familyID, familyName)
            self.cursor.execute(family_insert,values)
            self.cnx.commit()
            #family_data = (familyID,familyName)
            return familyID
        return familyName

    def edit_family(self, oldFamilyName, newFamilyName):
        new_family_ID = uuid.uuid4().hex
        get_family_info = ('Select * from family where familyName = ?', oldFamilyName)
        if get_family_info is not None:
            print('there is a family')
            family_update = self.query("UPDATE family SET familyName = ?, familyID = ?"
                                       , newFamilyName, new_family_ID)
            self.cnx.commit()
            return newFamilyName
        return newFamilyName

    def delete_family(self, deleteFamilyName):
        get_family_info = ('DELETE * from family where familyName = ?', deleteFamilyName)
        self.cursor.execute(get_family_info)
        self.cnx.commit()
        return deleteFamilyName

    def create_todo(self, description):
        staff_users_ID = uuid.uuid4().hex
        todo_id = random.randint(0,99999)
        if description is not None:
            todo_insert = ("INSERT INTO todos(toDoDescription,staffUsersID,todoID)values (?,?,?)")
            values = (description, staff_users_ID,todo_id)
            self.cursor.execute(todo_insert,values)
            self.cnx.commit()
            return staff_users_ID
        return description
    def getStates(self):
        try:
            self.cursor.execute("SELECT * FROM states")

            results = self.cursor.fetchall()

            states = {}

            for entry in results:

                country = entry[2].strip()
                if country not in states.keys():
                    states[country] = []

                states[country].append((entry[1], entry[0]))

            return states


        except Exception as e:
            print("Error retrieving states:")
            print(e)


    def get_user(self, user_data):
        user_data = {key:user_data[key] for key in ["userID", "username"] if key in user_data}

        user_query = "SELECT * FROM users WHERE " + " AND ".join([f"{key}='{value}'" for key, value in user_data.items()])
        print(user_query)

        try:
            self.cursor.execute(user_query)

            columns = [column[0] for column in self.cursor.description]
            
            user = self.cursor.fetchone()
            if user:
                return dict(zip(columns, user))
            else:
                return user
        except Exception as e:
            print("Error while retrieving user:")
            print(e)

    def get_like_users(self, user_data):
        user_data = {key:user_data[key] for key in ["userID", "username", "userAddress"] if key in user_data}

        user_query = "SELECT * FROM users WHERE " + " AND ".join([f"{key} LIKE '%{value}%'" for key, value in user_data.items()])
        print(user_query)

        try:
            self.cursor.execute(user_query)
            
            users = self.results_as_dict()

            return users
        except Exception as e:
            print("Error while retrieving multiple users:")
            print(e)

    def create_user(self, user_data):

        if any(key not in user_data for key in ["username", "userPassword"]):
            print("Missing user or password")
            return False

        for key in ["userAddress", "stateIDFK"]:
            if key not in user_data:
                user_data[key] = ""

        user_data["userID"] = uuid.uuid4().hex
                

        user_query = "INSERT INTO users(userID, username, userPassword, userAddress, stateIDFK) VALUES ('%(userID)s', '%(username)s', '%(userPassword)s', '%(userAddress)s', '%(stateIDFK)s')" % user_data
        
        user_data['myStudent'] = 1
        user_data["adminDashboard"] = 0

        for key in ["myStudent", "coachDashboard", "todosDashboard", "testPrepDashboard"]:
            if user_data['userRole'] in ["staff", "admin"]:
                user_data[key] = 1
            else:
                user_data[key] = 0

        if user_data['userRole'] == "admin":
            user_data["adminDashboard"] = 1


        if "familyID" in user_data.keys():
            user_data['isParent'] = 1
            second_query = "INSERT INTO parent(userIDFK, firstName, lastName, phoneNumber, email, familyIDFK) VALUES ('%(userID)s', '%(firstName)s', '%(lastName)s', '%(phoneNumber)s', '%(email)s', '%(familyID)s')" % user_data
        else:
            user_data['isParent'] = 0
            second_query = "INSERT INTO staff(userIDFK, firstName, lastName, phoneNumber, email) VALUES ('%(userID)s', '%(firstName)s', '%(lastName)s', '%(phoneNumber)s', '%(email)s')" % user_data


        perms_query = """INSERT INTO userPerms(myStudent, coachDashboard, adminDashboard, todosDashboard, testPrepDashboard, isParent, userIDFK)
                            VALUES('%(myStudent)s', '%(coachDashboard)s', '%(adminDashboard)s', '%(todosDashboard)s', '%(testPrepDashboard)s', '%(isParent)s', '%(userID)s')""" % user_data

        print(perms_query)

        try:
            self.cursor.execute(user_query)
            self.cursor.execute(second_query)
            self.cursor.execute(perms_query)
            self.cursor.commit()

            return True
        except Exception as e:
            print("Error while creating user:")
            print(e)


    def get_like_families(self, family_data = {}):
        family_data = {key:family_data[key] for key in ["familyID", "familyName"] if key in family_data}

        if len(family_data.keys()) < 1:
            family_query = "SELECT * FROM family"
        else:
            family_query = "SELECT * FROM family WHERE " + " AND ".join([f"{key} LIKE '%{value}%'" for key, value in family_data.items()])


        try:
            self.cursor.execute(family_query)
            
            families = self.results_as_dict()

            return families
        except Exception as e:
            print("Error while retrieving multiple users:")
            print(e)

    def get_coach_students(self, coachID):
        get_coach_students_query = """SELECT DISTINCT 
                                            student.firstName,
                                            student.lastName,
                                            student.school,
                                            student.familyIDFK,
                                            student.studentID
                                    FROM studentSessions
                                    LEFT JOIN student
                                    ON (student.studentID = studentSessions.studentIDFK)
                                    WHERE studentSessions.staffUsersIDFK = '%s'""" % coachID

        try:
            self.cursor.execute(get_coach_students_query)
            results = self.results_as_dict()

            return results
        except Exception as e:
            print("Error while retrieving coach students:")
            print(e)

    def get_like_staff(self, staff_data):
        if len(staff_data.keys()) > 0:
            staff_query = "SELECT * FROM staff WHERE " + " AND ".join([f"{key} LIKE '%{value}%'" for key, value in staff_data.items()])
        else:
            staff_query = "SELECT * FROM staff"

        try:
            self.cursor.execute(staff_query)
            
            staff = self.results_as_dict()

            return staff
        except Exception as e:
            print("Error while retrieving multiple staff:")
            print(e)

    def get_user_perms(self, userID):
        perms_query = "SELECT adminDashboard, myStudent, coachDashboard, todosDashboard, testPrepDashboard, isParent FROM userPerms WHERE userIDFK = ?"

        try:
            self.cursor.execute(perms_query, (userID, ))
            results = self.results_as_dict()
            return results
        except Exception as e:
            print("Error retrieving the user perms:")
            print(e)

    # function to query sql
    def query(self, sql):
        self.cursor.execute(sql)
        return self.results_as_dict()

    def create_session(self, new_session):
        new_session["sessionID"] = uuid.uuid4().hex
        session_insert = """INSERT INTO studentSessions(sessionID, programIDFK, sessionSubject, sessionDate, 
                                sessionHours, sessionsAttended, studentIDFK, staffUsersIDFK) Values (%(sessionID)s,%(programIDFK)s,%(sessionSubject)s,%(sessionDate)s,%(sessionHours)s,%(sessionAttended)s,
                                %(studentIDFK)s,%(staffUsersIDFK)s)"""% new_session
        try:
            self.cursor.execute(session_insert)
            self.cursor.commit()
            return True

        except Exception as e:
            print("Error inserting new session")
            print(e)
            return False



