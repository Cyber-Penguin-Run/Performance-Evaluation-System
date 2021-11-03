def connection():
    # server = 'CoT-CIS3365-10.cougarnet.uh.edu'
    database = 'Enrichery'
    username = 'Test'
    password = 'P@ssw0rd1'

    cnxn = "DRIVER={{SQL Server}};SERVER=CoT-CIS3365-10.cougarnet.uh.edu;DATABASE={};UID={};PWD={}".format(database, username, password)
    print(database)
    cursor = cnxn.cursor()

    sessions =cursor.execute("SELECT * FROM studentSessions;")

    connection()
    print(sessions)