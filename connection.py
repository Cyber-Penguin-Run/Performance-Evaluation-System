import pyodbc

class Database:
    def __init__(self):
        server = 'CoT-CIS3365-10.cougarnet.uh.edu'
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

        
