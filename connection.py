from flask.json import JSONEncoder, jsonify
import pyodbc
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
        
        user_data['studentDashboard'] = True

        for key in ["tutorDashboard", "staffDashboard", "businessDashboard", "studentProgress"]:
            if user_data['userRole'] == "admin":
                user_data[key] = True
            else:
                user_data[key] = False

        if "familyID" in user_data.keys():
            second_query = "INSERT INTO parent(userIDFK, firstName, lastName, phoneNumber, email, familyIDFK) VALUES ('%(userID)s', '%(firstName)s', '%(lastName)s', '%(phoneNumber)s', '%(email)s', '%(familyID)s')" % user_data
        else:
            
            second_query = "INSERT INTO staff(userIDFK, firstName, lastName, phoneNumber, email) VALUES ('%(userID)s', '%(firstName)s', '%(lastName)s', '%(phoneNumber)s', '%(email)s')" % user_data


        perms_query = """INSERT INTO userPerms(studentDashboard, tutorDashboard, staffDashboard, businessDashboard, studentProgress, userRole, userIDFK)
                            VALUES(%(studentDashboard)s, %(tutorDashboard)s, %(staffDashboard)s, %(businessDashboard)s, %(studentProgress)s, %(userRole)s, %(userID)s)""" % user_data

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

    # function to query sql
    def query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

