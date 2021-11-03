def connection():
    # server = 'CoT-CIS3365-10.cougarnet.uh.edu'
    database = 'Enrichery'
    username = 'Test'
    password = 'P@ssw0rd1'

    # cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    # cursor = cnxn.cursor()

    # cursor.execute("SELECT * FROM staff;")

    cnxn = "DRIVER={{SQL Server}};SERVER=CoT-CIS3365-10.cougarnet.uh.edu;DATABASE={};UID={};PWD={}".format(database, username, password)
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM staff;")

    connection()