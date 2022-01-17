import sqlite3

con = sqlite3.connect('database.db')
print ("Opened database successfully")
con.execute('''
            DROP TABLE employee_info;
        ''')
con.execute('''
            CREATE TABLE employee_info (
                employee_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                employee_name varchar NOT NULL,
                gender varchar NOT NULL,
                email varchar NOT NULL,
                address varchar NOT NULL,
                Academic_qualification varchar NOT NULL,
                Username varchar NOT NULL,
                Password varchar NOT NULL
            );
        ''')
con.execute('''
            DROP TABLE admin_auth;
        ''')
con.execute('''
            CREATE TABLE admin_auth (
                Username varchar NOT NULL,
                Password varchar NOT NULL
            );
        ''')
cursor = con.cursor()
cursor.execute("INSERT INTO admin_auth ( Username, Password) VALUES('admin', 'admin');")
print ("Table created successfully")
con.commit()
con.close()
