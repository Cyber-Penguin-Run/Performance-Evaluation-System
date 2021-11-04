from flask.json import JSONEncoder, jsonify
import pyodbc
import json
import uuid


class Database:
    def __init__(self):
        server = 'CoT-CIS3365-10.cougarnet.uh.edu'
        database = 'Enrichery'
        username = 'Test'
        password = 'P@ssw0rd1'

        try:
            self.cnx = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
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
        user_data = {key: user_data[key] for key in ["userID", "username"] if key in user_data}

        user_query = "SELECT * FROM users WHERE " + " AND ".join(
            [f"{key}='{value}'" for key, value in user_data.items()])
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
        user_data = {key: user_data[key] for key in ["userID", "username", "userAddress"] if key in user_data}

        user_query = "SELECT * FROM users WHERE " + " AND ".join(
            [f"{key} LIKE '%{value}%'" for key, value in user_data.items()])
        print(user_query)

        try:
            self.cursor.execute(user_query)

            users = db.results_as_dict()

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

        try:
            self.cursor.execute(user_query)
            self.cursor.commit()
        except Exception as e:
            print("Error while creating user:")
            print(e)
        else:
            return True

db = Database()
#print(db.get_like_users())
#print(db.get_user({"userID":"db498e04ab7046cf91fc17e34c425466", "username":"bmeagherw"}))