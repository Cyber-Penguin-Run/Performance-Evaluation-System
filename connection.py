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


    def create_family(self, familyName, familyStatus):
        familyID = uuid.uuid4().hex

        if familyName is not None:
            family_insert = ("INSERT INTO family(familyID, familyName, familyStatus)"
                                       "Values (?, ?, ?)")
            try:
                values = (familyID, familyName, familyStatus)
                self.cursor.execute(family_insert,values)
                self.cnx.commit()
                
                return familyID
            except Exception as e:
                print("Error creating new family:")
                print(e)
                return None
        return None

    def edit_family(self, familyID, newFamilyName, familyStatus):
        get_family_info = ("Select * from family where familyID = '%s'" % familyID)
        if get_family_info is not None:
            family_update = "UPDATE family SET familyName = '%s', familyStatus='%s' WHERE familyID = '%s'" % (newFamilyName, familyStatus, familyID)
            self.cursor.execute(family_update)
            self.cnx.commit()
            return newFamilyName
        return newFamilyName

    def delete_family(self, familyID):
        find_orphans = f"SELECT studentID FROM student WHERE familyIDFK = '{familyID}'"
        find_parents = f"SELECT userIDFK from parent WHERE familyIDFK = '{familyID}'"
        delete_family = f"DELETE FROM family where familyID = '{familyID}'"
        try:
            orphans = self.query(find_orphans)
            parents = self.query(find_parents)

            if len(orphans) > 0:
                create_orphans = "UPDATE student SET familyIDFK = NULL WHERE studentID IN (%s)" % ", ".join([f"'{orphan['studentID']}'" for orphan in orphans])
                print(create_orphans)
                self.cursor.execute(create_orphans)

            if len(parents) > 0:
                kill_parents = "UPDATE parent SET familyIDFK = NULL WHERE userIDFK IN (%s)" % ", ".join([f"'{parent['userIDFK']}'" for parent in parents])
                print(kill_parents)
                self.cursor.execute(kill_parents)

            self.cursor.execute(delete_family)
            self.cnx.commit()
            return True

        except Exception as e:
            print("Error deleting family: ")
            print(e)
            return False

    def delete_staff(self, staffID):
        delete_query = f"DELETE FROM parent WHERE userIDFK = '{staffID}'"
        user_delete = f"DELETE FROM users WHERE userID = '{staffID}'"
        userperm_delete = f"DELETE FROM userPerms WHERE userIDFK = '{staffID}'"
        try:
            self.cursor.execute(delete_query)
            self.cursor.execute(userperm_delete)
            self.cursor.execute(user_delete)
            self.cnx.commit()
            return True
        except Exception as e:
            print('error during delete staff', e)
            return False

    def delete_parent(self, parentID):
        delete_query = f"DELETE FROM parent WHERE userIDFK = '{parentID}'"
        user_delete = f"DELETE FROM users WHERE userID = '{parentID}'"
        userperm_delete = f"DELETE FROM userPerms WHERE userIDFK = '{parentID}'"
        try:
            self.cursor.execute(delete_query)
            self.cursor.execute(userperm_delete)
            self.cursor.execute(user_delete)
            self.cnx.commit()
            return True
        except Exception as e:
            print('error during delete parent', e)
            return False

    def delete_student(self, studentID):
        delete_query = f"DELETE FROM student WHERE studentID = '{studentID}'"
        try:
            print(delete_query)
            self.cursor.execute(delete_query)
            self.cnx.commit()
            return True
        except Exception as e:
            print('error during delete student', e)
            return False

    def get_todos(self, staffID):
        todo_query = f"""SELECT * FROM todos
                            LEFT JOIN staff
                            ON (todos.staffUsersID = staff.userIDFK)
                            WHERE staff.userIDFK LIKE '%{staffID}%'"""

        return self.query(todo_query)

    def create_todo(self,staffID, description):
        todo_id = uuid.uuid4().hex
        if description is not None:
            todo_insert = ("INSERT INTO todos(toDoDescription,staffUsersID,todoID)values (?,?,?)")
            values = (description, staffID,todo_id)
            try:
                self.cursor.execute(todo_insert,values)
                self.cnx.commit()
                return True
            except Exception as e:
                print('error during insert todo', e)
                return False

    def delete_todo(self,todoID):
        todo_delete = "DELETE FROM todos WHERE todoID = '%s'" % todoID
        try:
            self.cursor.execute(todo_delete)
            self.cnx.commit()
            return True
        except Exception as e:
            print('error during deletion of todo', e)
            return False

    def update_todo(self,toDoDescription, todoID):
        update_todo = "UPDATE todos set toDoDescription = '%s' WHERE todoID = '%s' " % (toDoDescription,todoID)
        try:
            print(update_todo)
            self.cursor.execute(update_todo)
            self.cursor.commit()
            return True
        except Exception as e:
            print('error during deletion of todo', e)
            return False

    def create_mock(self,mockType,mockInfo):
        mock_score_id = uuid.uuid4().hex
        if mockType == 'act':
            mockInfo['actScoreID'] = mock_score_id
            mock_insert = """INSERT INTO mockActScores(actScoreID,studentIDFK,englishScore,englishMax,mathScore,mathMax,
                          readingScore,readingMax,scienceScore,scienceMax,actCompScore,actType,actTestDate) values
                          ('%(actScoreID)s','%(studentIDFK)s','%(englishScore)s','%(englishMax)s','%(mathScore)s',
                          '%(mathMax)s','%(readingScore)s','%(readingMax)s','%(scienceScore)s','%(scienceMax)s',
                          '%(actCompScore)s','%(actType)s','%(actTestDate)s')""" % mockInfo
        elif mockType == 'sat':
            mockInfo['satScoreID'] = mock_score_id
            mock_insert = """INSERT INTO mockSatScores(satScoreID,studentIDFK,writingScore,writingMax,mathCalcScore,mathCalcMax,
                              mathScore,mathMax,readingScore,readingMax,satCompScore,satType,satTestDate) values
                              ('%(satScoreID)s','%(studentIDFK)s','%(writingScore)s','%(writingMax)s','%(mathCalcScore)s',
                              '%(mathCalcMax)s','%(mathScore)s', '%(mathMax)s','%(readingScore)s','%(readingMax)s',
                              '%(satCompScore)s','%(satType)s','%(satTestDate)s')""" % mockInfo
        elif mockType == 'hspt':
            mockInfo['hsptScoreID'] = mock_score_id
            mock_insert = """INSERT INTO mockhsptScores(hsptScoreID,studentIDFK,englishScore,englishMax,mathScore,mathMax,
                              readingScore,readingMax,scienceScore,scienceMax,actCompScore,actType,actTestDate) values
                              ('%(hsptScoreID)s','%(studentIDFK)s','%(englishScore)s','%(englishMax)s','%(mathScore)s',
                              '%(mathMax)s','%(readingScore)s','%(readingMax)s','%(scienceScore)s','%(scienceMax)s',
                              '%(actCompScore)s','%(actType)s','%(actTestDate)s')""" % mockInfo
        if mockType == 'isee':
            mockInfo['iseeScoreID'] = mock_score_id
            mock_insert = """INSERT INTO mockActScores(actScoreID,studentIDFK,englishScore,englishMax,mathScore,mathMax,
                              readingScore,readingMax,scienceScore,scienceMax,actCompScore,actType,actTestDate) values
                              ('%(iseeScoreID)s','%(studentIDFK)s','%(englishScore)s','%(englishMax)s','%(mathScore)s',
                              '%(mathMax)s','%(readingScore)s','%(readingMax)s','%(scienceScore)s','%(scienceMax)s',
                              '%(actCompScore)s','%(actType)s','%(actTestDate)s')""" % mockInfo
        try:
            print("executing mock query")
            print(mock_insert)
            self.cursor.execute(mock_insert)
            self.cursor.commit()
            return True
        except Exception as e:
            print('error during insertion of act mock', e)
            return False

    def delete_mock(self,mockType,mockID):
        if mockType == 'sat':
            mock_delete = "DELETE FROM mockSatScores WHERE satScoreID = '%s'" % mockID
        if mockType == 'act':
            mock_delete = "DELETE FROM mockActScores WHERE actScoreID = '%s'" % mockID
        if mockType == 'isee':
            mock_delete = "DELETE FROM mockIseeScores WHERE iseeScoreID = '%s'" % mockID
        if mockType == 'hspt':
            mock_delete = "DELETE FROM mockHsptScores WHERE hsptScoreID = '%s'" % mockID
        try:
            self.cursor.execute(mock_delete)
            self.cnx.commit()
            return True
        except Exception as e:
            print('error during deletion of todo', e)
            return False

    def update_mock(self,mockType,examID, mock_info):
        if mockType == 'sat':
            mock_update = "UPDATE mockSatScores SET " + ", ".join([f"{column} = '{value}'" for column, value in mock_info.items() if value != ""]) + " WHERE satScoreID = '%s'" % examID
        elif mockType == 'act':
            pass
        elif mockType == 'hspt':
            pass
        elif mockType == 'isee':
            pass
        try:
            self.cursor.execute(mock_update)
            self.cnx.commit()
            return True
        except Exception as e:
            print('error during deletion of todo', e)
            return False

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

        user_query = "SELECT * FROM staff LEFT JOIN users ON (staff.userIDFK = users.userID) LEFT JOIN userPerms ON (users.userID = userPerms.userIDFK) WHERE " + " AND ".join([f"{key} LIKE '%{value}%'" for key, value in user_data.items()])

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


    def get_coach_assignments(self, coachID):
        coach_assignments_query = f"""SELECT assignments.assignmentID,
                                            assignments.assignmentDate,
                                            assignments.assignmentGrade,
                                            assignments.assignmentType,
                                            student.firstName,
                                            student.lastName
                                        FROM assignments
                                        LEFT JOIN student
                                        ON (student.studentID = assignments.studentIDFK)
                                        WHERE assignments.staffUsersIDFK LIKE '%{coachID}%'"""
        
        return self.query(coach_assignments_query)

    def get_coach_information(self, coachID):
        specific_coach = f"""SELECT staff.*, 
                                    users.userAddress,
                                    states.stateName,
                                    states.countryName
                                    FROM staff 
                                    LEFT JOIN users 
                                    ON(staff.userIDFK = users.userID)
                                    LEFT JOIN states
                                    ON (users.stateIDFK = states.stateID)
                                    WHERE staff.userIDFK LIKE '%{coachID}%'"""

        return self.query(specific_coach)

    def create_session(self, new_session):
        new_session["sessionID"] = uuid.uuid4().hex

        if new_session['sessionAttended'] == "":
            new_session['sessionAttended'] = 0

        session_insert = """INSERT INTO studentSessions(sessionID, programIDFK, sessionSubject, sessionDate, 
                                sessionHours, sessionAttendedHours, studentIDFK, staffUsersIDFK) Values ('%(sessionID)s','%(programIDFK)s','%(sessionSubject)s','%(sessionDate)s','%(sessionHours)s','%(sessionAttended)s',
                                '%(studentIDFK)s','%(staffUsersIDFK)s')"""% new_session
        try:
            print(session_insert)
            self.cursor.execute(session_insert)
            self.cursor.commit()
            return True

        except Exception as e:
            print("Error inserting new session")
            print(e)
            return False

    def get_coach_students_fullname(self, coachID, fullname):

        fullname_query = f"""SELECT s.firstName, s.lastName, s.school, s.studentID, s.familyIDFK, concat(s.firstName , ' ' , s.lastName) AS FullName
                                FROM student AS s
                                RIGHT JOIN studentSessions
                                ON (s.studentID = studentSessions.studentIDFK)
                                WHERE studentSessions.staffUsersIDFK LIKE '%{coachID}%'
                                AND concat(s.firstName , ' ' , s.lastName) LIKE '%{fullname}%'"""

        try:
            self.cursor.execute(fullname_query)
            results = self.results_as_dict()

            return results
        except Exception as e:
            print("Error while retrieving coach fullname students:")
            print(e)

    def get_students_fullname(self, fullname):
        fullname_query = f"""SELECT s.firstName, s.lastName, s.school, s.studentID, s.familyIDFK, concat(s.firstName , ' ' , s.lastName) AS FullName
                                FROM student AS s
                                WHERE concat(s.firstName , ' ' , s.lastName) LIKE '%{fullname}%'"""

        try:
            self.cursor.execute(fullname_query)
            results = self.results_as_dict()

            return results
        except Exception as e:
            print("Error while retrieving coach fullname students:")
            print(e)


    def get_staff_fullname(self, fullname):

        fullname_query = f"""SELECT s.*, users.*, concat(s.firstName , ' ' , s.lastName) AS FullName
                                FROM staff AS s
                                RIGHT JOIN users
                                ON (s.userIDFK = users.userID)
                                WHERE concat(s.firstName , ' ' , s.lastName) LIKE '%{fullname}%'"""

        try:
            self.cursor.execute(fullname_query)
            results = self.results_as_dict()

            return results
        except Exception as e:
            print("Error while retrieving coach fullname students:")
            print(e)


    def get_families_fullname(self, fullname):

        fullname_query = f"""SELECT f.*
                                FROM family AS f
                                WHERE f.familyName LIKE '%{fullname}%'"""

        try:
            self.cursor.execute(fullname_query)
            results = self.results_as_dict()

            return results
        except Exception as e:
            print("Error while retrieving families:")
            print(e)

    def get_student_assignments(self, studentID):
        assignments_query = """SELECT * FROM assignments WHERE assignments.studentIDFK = '%s'""" % studentID 
        
        return self.query(assignments_query)

    def get_student(self, studentID):
        student_query = "SELECT * FROM student WHERE student.studentID = '%s'" % studentID

        return self.query(student_query)

    def create_assignment(self, staffID, studentID, assignment_info):
        assignment_query = "INSERT INTO assignments(assignmentDate, assignmentType, assignmentID, staffUsersIDFK, studentIDFK) VALUES ('%s', '%s', '%s', '%s', '%s')"

        assignmentID = uuid.uuid4().hex

        assignment_query = assignment_query % (assignment_info['assignmentDate'], assignment_info['assignmentType'], assignmentID, staffID, studentID)

        try:
            print(assignment_query)
            self.cursor.execute(assignment_query)
            self.cursor.commit()
        except Exception as e:
            print("Error creating assignment:")
            print(e)

    def delete_assignment(self, assignmentID):
        delete_query = f"DELETE FROM assignments WHERE assignmentID = '{assignmentID}'"
        try:
            self.cursor.execute(delete_query)
            self.cursor.commit()
        except Exception as e:
            print("Error deleting assignment:")
            print(e)

    def delete_session(self, sessionID):
        delete_query = f"DELETE FROM studentSessions WHERE sessionID = '{sessionID}'"
        try:
            self.cursor.execute(delete_query)
            self.cursor.commit()
        except Exception as e:
            print("Error deleting session:")
            print(e)

    def update_assignment(self, assignmentID, assignment_info):
        update_query = "UPDATE assignments SET " + ", ".join([f"{key} = '{value}'" for key, value in assignment_info.items() if value != ""]) + f" WHERE assignmentID = '{assignmentID}'"

        try:
            self.cursor.execute(update_query)
            self.cursor.commit()
        except Exception as e:
            print("Error updating assignment: ")
            print(e)

    def update_session(self, sessionID, session_info):
        update_query = "UPDATE studentSessions SET " + ", ".join([f"{key} = '{value}'" for key, value in session_info.items() if value != ""]) + f" WHERE sessionID = '{sessionID}'"

        try:
            self.cursor.execute(update_query)
            self.cursor.commit()
        except Exception as e:
            print("Error updating session: ")
            print(e)

    def get_student_sessions(self, studentID):
        assignments_query = """SELECT * FROM studentSessions WHERE studentSessions.studentIDFK = '%s'""" % studentID 
        
        return self.query(assignments_query)

    def get_coach_families(self, coachID):
        families_query = f"""SELECT * FROM studentSessions
                                    LEFT JOIN student
                                    ON (student.studentID = studentSessions.studentIDFK)
                                    RIGHT JOIN family
                                    ON (family.familyID = student.familyIDFK)
                                    WHERE studentSessions.staffUsersIDFK LIKE '%{coachID}%'"""

        return self.query(families_query)

    def get_family(self, familyID):
        family_query = f"SELECT * FROM family WHERE familyID = '{familyID}'"


        try:
            family = self.query(family_query)[0]
            family['exists'] = True
        except IndexError:
            family = {}
            family['exists'] = False

        family['parents'] = self.query(f"SELECT * FROM parent WHERE familyIDFK = '{familyID}'")
        family['students'] = self.query(f"SELECT * FROM student WHERE familyIDFK = '{familyID}'")

        print(family['parents'])

        return family
        

    def get_coach_like_families(self, coachID, familyName):
        families_query = f"""SELECT * FROM studentSessions
                                    LEFT JOIN student
                                    ON (student.studentID = studentSessions.studentIDFK)
                                    RIGHT JOIN family
                                    ON (family.familyID = student.familyIDFK)
                                    WHERE studentSessions.staffUsersIDFK LIKE '%{coachID}%'
                                    AND family.familyName LIKE '%{familyName}%'"""

        return self.query(families_query)

    def get_student_programs(self, studentID):
        programs_query = f"SELECT * FROM studentPrograms WHERE studentIDFK = '{studentID}'"

        return self.query(programs_query)

    def update_coach_information(self, coachID, coach_info):
        update_staff = "UPDATE staff SET " + ", ".join([f"{key} = '{value}'" for key, value in coach_info.items() if value != "" and key in ["firstName", "lastName", "phoneNumber", "email"]]) + f" WHERE staff.userIDFK = '{coachID}'"

        update_user = "UPDATE users SET " + ", ".join([f"{key} = '{value}'" for key, value in coach_info.items() if value != "" and key in ["userAddress", "stateIDFK"]]) + f" WHERE users.userID = '{coachID}'"

        try:
            print(update_staff)
            print(update_user)
            self.cursor.execute(update_staff)
            self.cursor.execute(update_user)
            self.cursor.commit()
            return True
        except Exception as e:
            print("Error updating coach information: ")
            print(e)

    def create_student(self, student_info):
        student_info["studentID"] = uuid.uuid4().hex

        keys = student_info.keys()

        student_insert = f"""INSERT INTO student({', '.join(keys)}) Values ({', '.join([f"'{student_info[key]}'" for key in keys ])})"""

        try:
            print(student_insert)
            self.cursor.execute(student_insert)
            self.cursor.commit()
            return True

        except Exception as e:
            print("Error inserting new session")
            print(e)
            return False
