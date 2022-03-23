# Name: Lee Hui Ying
# Matric no.: 149044


# Import Libraries
import sqlite3
from flask import Flask, redirect, url_for, render_template, request, session, flash,  jsonify
from flask_restful import Resource, Api
import requests

# _________________________ SQLite Database ___________________________

# A databaset only run on the first time to create 2 tables with correct attributes to store the 
# Admin information and employee information
def database_start():

    # Connect database
    con = sqlite3.connect('database.db')

    # A message is printed for checking purpose
    print("Opened database successfully")

    # Execute sql command to drop the existing table with same table name
    con.execute('''
            DROP TABLE employee_info;
        ''')

    # Execute sql command to create employee_info table to store employee information
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

    # Execute sql command to drop the existing table with same table name
    con.execute('''
            DROP TABLE admin_auth;
        ''')

    # Execute sql command to create admin_auth table to store admin information
    con.execute('''
            CREATE TABLE admin_auth (
                Username varchar NOT NULL,
                Password varchar NOT NULL
            );
        ''')
    
    # Create cursor as connection object
    cursor = con.cursor()

    # Execute sql command to insert admin username = 'admin' and admin password = 'admin' as default admin
    cursor.execute(
        "INSERT INTO admin_auth ( Username, Password) VALUES('admin', 'admin');")
    print("Table created successfully")

    # Commit sql  command  and close it
    con.commit()
    con.close()

# Create database connection to 'database.db'
def database_connection():
    con = sqlite3.connect('database.db')
    return con

# Add employee into the database
def add_emp(emp):

    # Create empty list
    add_employee = {}
    try:

        # Create database connection and connection object
        con = database_connection()
        cursor = con.cursor()

        # Search an employee with a username and return the one result
        cursor.execute("SELECT * FROM employee_info WHERE Username = ? ",
                       (emp['emp_username'],))
        i = cursor.fetchone()

        # Convert the employee address to uppercase
        emp['emp_address'] = emp['emp_address'].upper()

        # If the username is not exist, execute sql command to insert the employee information into the database
        if not i:
            cursor.execute("INSERT INTO employee_info ( Username, Password, employee_name, gender, Academic_qualification, email, address ) VALUES(?, ?, ?, ?, ?, ?, ?)",
                           (emp['emp_username'], emp['emp_password'], emp['emp_name'], emp['gender'], emp['academic'], emp['email'], emp['emp_address']))

        # else, return False
        else:
            return False

        # Commit sql command and search the last employee using the last row id
        con.commit()
        add_employee = get_emp_by_id(cursor.lastrowid)

    # Error handler
    except:
        con().rollback()

    # Close connection
    finally:
        con.close()

    # return the employee information in dict
    return add_employee

# Retrieve all the employees
def get_emp():

    # Create empty array
    employees = []
    try:
        # Create database connection and select all the employee information, then return row objects
        con = database_connection()
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("SELECT * FROM employee_info")
        all = cursor.fetchall()

        # Convert row objects to dictionary
        for i in all:
            emp = {}
            emp["emp_id"] = i["employee_id"]
            emp["name"] = i["employee_name"]
            emp["gender"] = i["gender"]
            emp["email"] = i["email"]
            emp["address"] = i["address"]
            emp["academic"] = i["Academic_qualification"]
            emp["username"] = i["Username"]
            emp["password"] = i["Password"]
            employees.append(emp)

    # Error handler
    except:
        employees = []

    # Close connection
    finally:
        con.close()

    # return the all employee information in array
    return employees

# Retrieve an employee using an employee id
def get_emp_by_id(emp_id):

    # Create empty list
    emp = {}
    try:

        # Create database connection and select an employee information using employee id, 
        # then return row object
        con = database_connection()
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("SELECT * FROM employee_info WHERE employee_id = ?",
                       (emp_id,))
        i = cursor.fetchone()

        # Convert row object to dictionary
        emp = {}
        emp["emp_id"] = i["employee_id"]
        emp["name"] = i["employee_name"]
        emp["gender"] = i["gender"]
        emp["email"] = i["email"]
        emp["address"] = i["address"]
        emp["academic"] = i["Academic_qualification"]
        emp["username"] = i["Username"]
        emp["password"] = i["Password"]

    # Error handler
    except:
        emp = {}

    # Close connection
    finally:
        con.close()

    # return the an employee information in dictionary
    return emp

# Update an employee information
def update_emp(emp):

    # Create empty list
    update_emp = {}
    try:
        # Creat database connection and connection object
        con = database_connection()
        cursor = con.cursor()

        # Convert the employee address to uppercase
        emp['emp_address'] = emp['emp_address'].upper()

        # Update the employee information into the database and commit the sql command
        cursor.execute("UPDATE employee_info SET employee_name= ?, gender= ?, email= ?, address= ?,Academic_qualification= ?, Password =? WHERE employee_id=?",
                       (emp['emp_name'], emp['gender'], emp['email'], emp['emp_address'], emp['academic'], emp['emp_password'], emp['emp_id']))
        con.commit()

        # Retrieve an employee information using employee id
        update_emp = get_emp_by_id(emp['emp_id'])

    # Error handler
    except:
        con.rollback()
        update_emp = {}

    # Close connection
    finally:
        con.close()

    # Return the updated employee information
    return update_emp

# Delete an employee information using employee id
def delete_emp(emp_id):
    # Create empty list to store the message
    message = {}

    try:
        # Create database connection and execute delete sql command and commit the sql command
        con = database_connection()
        con.execute("DELETE from employee_info WHERE employee_id = ?",
                    (emp_id,))
        con.commit()

        # D=Generate a message
        message["status"] = "Employee is deleted successfully"

    # Error handler
    except:
        con.rollback()
        message["status"] = "Cannot delete employee"

    # Close database
    finally:
        con.close()

    # Return message
    return message

# Add admin into the database


def add_admin(admin_username, admin_password):
    # Create empty list
    admin = {}
    try:
        # Create database connection and connection object
        con = database_connection()
        cursor = con.cursor()

        # Search an employee with a username and return the one result
        cursor.execute("SELECT * FROM admin_auth WHERE Username = ? ",
                       (admin_username,))
        i = cursor.fetchone()

        # If the username is not exist, execute sql command to insert the employee information into the database
        if not i:
            cursor.execute("INSERT INTO admin_auth ( Username, Password) VALUES(?, ?)",
                           (admin_username, admin_password))

        # else, return False
        else:
            return False

         # Commit sql command
        con.commit()

        # Group admin information into a list
        admin = {}
        admin["username"] = admin_username
        admin["password"] = admin_password

    # Error handler
    except:
        con().rollback()

    # Close database
    finally:
        con.close()

    # return admin information
    return admin

# Employee login Checking using username and password
def login_emp(username, password):
    # Create empty list
    emp = {}
    try:
        # Create database connection and select an employee information using username and password,
        # then return row object
        con = database_connection()
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("SELECT * FROM employee_info WHERE Username = ? AND Password = ?",
                       (username, password,))
        i = cursor.fetchone()

        # Convert row object to dictionary
        emp = {}
        emp["emp_id"] = i["employee_id"]
        emp["name"] = i["employee_name"]
        emp["gender"] = i["gender"]
        emp["email"] = i["email"]
        emp["address"] = i["address"]
        emp["academic"] = i["Academic_qualification"]
        emp["username"] = i["Username"]
        emp["password"] = i["Password"]

    # Error handler
    except:
        return False

    # Close database
    finally:
        con.close()

    # return the employee information
    return emp

# Admin login Checking using username and password
def login_admin(username, password):
    # Create empty list
    admin = {}
    try:
        # Create database connection and select an admin information using username and password,
        # then return row object
        con = database_connection()
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("SELECT * FROM admin_auth WHERE Username = ? AND Password = ?",
                       (username, password,))
        i = cursor.fetchone()

        # Convert row object to dictionary
        admin = {}
        admin["username"] = i["Username"]
        admin["password"] = i["Password"]

    # Error handler
    except:
        return False

    # Close database
    finally:
        con.close()

    # return admin information
    return admin


app = Flask(__name__)
app.secret_key = "Hello"
api = Api(app)


# _________________________ REST API ___________________________

# Resource base class generated to route for one or more HTTP methods for a given URL

# All employee
class api_all_emp(Resource):

    # Retrieve list of employees
    def get(self):
        return jsonify(get_emp())

# Employee
class api_emp(Resource):

    # Create a new employee
    def post(self):
        emp = request.get_json()
        return jsonify(add_emp(emp))

    # Retrieve an employee
    def get(self):
        emp_id = request.args.get('emp_id')
        return jsonify(get_emp_by_id(emp_id))

    # Update an existing employee
    def put(self):
        emp = request.get_json()
        return jsonify(update_emp(emp))

    # Delete an employee
    def delete(self):
        emp_id = request.args.get('emp_id')
        return jsonify(delete_emp(emp_id))

# Admin
class api_admin(Resource):
    # Create a new employee
    def post(self):
        admin = request.get_json()
        return jsonify(add_admin(admin))

# Login
class api_login(Resource):
    # Login information checking
    def get(self):
        submit = request.args.get('submit')

        # employee login
        if submit == "Employee":
            print('hi')
            emp_username = request.args.get('emp_username')
            emp_password = request.args.get('emp_password')
            return jsonify(login_emp(emp_username, emp_password))

        # admin login
        else:
            admin_username = request.args.get('admin_username')
            admin_password = request.args.get('admin_password')
            return jsonify(login_admin(admin_username, admin_password))


# add_resource function registers the routes with the framework using the given endpoint
api.add_resource(api_all_emp, '/emp_all')                       # get all employee
api.add_resource(api_emp, '/add_emp', endpoint='post')          # create new employee
api.add_resource(api_emp, '/emp/get', endpoint='get')           # get an employee
api.add_resource(api_emp, '/emp/put', endpoint='put')           # update existing employee
api.add_resource(api_emp, '/emp/delete', endpoint='delete')     # delete an employee
api.add_resource(api_admin, '/add_admin')                       # add admin
api.add_resource(api_login, '/api/login')                       # login


# _________________________ Flask ___________________________

# Route to Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Route to Signup for employee
@app.route("/signup_emp/", methods=["POST", "GET"])
def signup_emp():
    if request.method == "POST":
        # get the form information
        emp = jsonify(request.form).json

        # check if the academic part is not empty
        academic = request.form["academic"]
        if academic != "NONE":
            # execute post method
            emp=requests.post('http://127.0.0.1:5000/add_emp',json=emp).json()

            # check if the username existed then go back to signup page
            if emp == False:
                flash('The username is existed!')
                return render_template("signup_emp.html")

            # else, generate session and go to employee profile
            else:
                session.permanent = True  # <--- makes the permanent session
                session["emp_username"] = emp['username']
                session["emp_password"] = emp['password']
                session["emp_id"] = emp['emp_id']
                return redirect(url_for("employee"))

        # if academic part in the form is empty, go back to signup page and display a warning
        else:
            flash('The Academic_qualification field cannot be empty !')
            return render_template("signup_emp.html")

    else:
        return render_template("signup_emp.html")

# Route to Signup for admin
@app.route("/signup_admin", methods=["POST", "GET"])
def signup_admin():
    if request.method == "POST":
        # get the form information and execute post method
        admin = jsonify(request.form).json
        admin = requests.post('http://127.0.0.1:5000/add_admin', json=admin).json()

        # check if the admin username existed go to signup_admin page
        if admin == False:
            flash('The username is existed!')
            return render_template("signup_admin.html")

        # else, generate a session and go to admin profile
        else:
            session.permanent = True  # <--- makes the permanent session
            session["admin_username"] = admin['admin_username']
            session["admin_password"] = admin['admin_password']
            return redirect(url_for("admin"))
    else:
        return render_template("signup_admin.html")

# Route to employee profile
@app.route("/employee")
def employee():

    # if the user is employee, get the employee id to execute get method then go to employee profile
    if "emp_username" in session:
        emp_id = session["emp_id"]
        emp = requests.get(
            'http://127.0.0.1:5000/emp/get', params={'emp_id': emp_id}).json()
        return render_template("employee.html", emp=emp)

    # else if the user is admin, get the employee id to execute get method 
    elif "admin_username" in session:
        emp_id = session["emp_id"]
        emp = requests.get(
            'http://127.0.0.1:5000/emp/get', params={'emp_id': emp_id}).json()

        # if the employee exists, then go to employee profile
        if emp != {}:
            return render_template("employee.html", emp=emp)

        # else pop out the session, go to employee_list page and display a message
        else:
            session.pop("emp_id", None)
            flash('The employee ID does not exist !')
            return redirect(url_for("employee_list"))
    else:
        return redirect(url_for("login"))

# Route to update employee
@app.route('/updateEmployee', methods=["POST", "GET"])
def updateEmployee():
    if request.method == "POST":
        # get the employee id and the input form information and combine to one dictionary file,
        # then execute put method
        emp_id = session["emp_id"]
        emp = jsonify(request.form).json
        emp_id = {'emp_id':emp_id}
        emp.update(emp_id)
        emp = requests.put(
            'http://127.0.0.1:5000/emp/put', json=emp).json()

        # display message based on the information is updated or not, then go to employee profile
        if emp != {}:
            flash('The employee is updated !')
        else:
            flash('The employee cannot be updated !')
        return redirect(url_for("employee"))

    else:

        # if it is not post method, get the employee id to execute get method, then go to update page
        emp_id = session["emp_id"]
        emp = requests.get(
            'http://127.0.0.1:5000/emp/get', params={'emp_id': emp_id}).json()
        return render_template("update.html", emp=emp)

# Route to login as admin
@app.route("/admin")
def admin():
    if "admin_username" in session:
        # if the admin_username in session, set the session, then go to admin profile
        session.permanent = True  # <--- makes the permanent session
        admin_username = session["admin_username"]
        admin_password = session["admin_password"]
        return render_template("admin.html", admin=admin_username, password=admin_password)

    # else, logout and go to login page
    else:
        return redirect(url_for("login"))

# Route to employee_list page
@app.route('/employeeList')
def employee_list():
    # execute get method, then go to employee_list page
    emp = requests.get(
        'http://127.0.0.1:5000/emp_all').json()
    return render_template("employee_list.html", emp=emp)

# Route to search employee
@app.route('/searchEmployee', methods=["POST"])
def searchEmployee():

    # get the employee id from the form, set the employee id session and go to employee profile
    emp_id = request.form["emp_id"]
    session["emp_id"] = emp_id
    return redirect(url_for("employee"))

# Route to add employee
@app.route("/addEmployee", methods=["POST", "GET"])
def add_employee():
    if request.method == "POST":
        # get the input form information
        emp = jsonify(request.form).json

        # check if the academic part is not empty
        academic = request.form["academic"]
        if academic != "NONE":

            # execute post method
            emp = requests.post(
                'http://127.0.0.1:5000/add_emp', json=emp).json()

            # check if the username existed then go back to add_emp page
            if emp == False:
                flash('The username is existed!')
                return render_template("add_emp.html")

            # else, get the employee id, then go to employee profile page and display a message
            else:
                emp_id = emp['emp_id']
                session["emp_id"] = emp_id
                flash('An employee is added !')
                return redirect(url_for("employee"))

        # if academic part in the form is empty, go back to add_emp page and display a warning
        else:
            flash('The Academic_qualification field cannot be empty !')
            return render_template("add_emp.html")
    else:
        return render_template("add_emp.html")

# Route to delete employee
@app.route('/deleteEmployee', methods=["POST"])
def deleteEmployee():
    # get employee id from the form, pop out the employee id session, execute delete method,
    # go back to employee list page with a message displayed
    emp_id = request.form["emp_id"]
    session.pop("emp_id", None)
    message = requests.delete(
        'http://127.0.0.1:5000/emp/delete', params={'emp_id': emp_id}).json()
    message = message["status"]
    flash(message)
    return redirect(url_for("employee_list"))

# Route to login page
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # if employee button is clicked on
        if request.form["submit"] == "Employee":

            # get the form input information and execute get method
            emp = jsonify(request.form).json
            emp = requests.get(
                'http://127.0.0.1:5000/api/login', params={'submit':emp['submit'],'emp_username': emp['username'], 'emp_password': emp['password']}).json()

            # if the username and password, go back to login page and display warning message
            if emp == False:
                flash('The username or password is incorrect !')
                return render_template("login.html")

            # else, set the session and go to employee profile page
            else:
                session["emp_id"] = emp['emp_id']
                session["emp_username"] = emp['username']
                return redirect(url_for("employee"))

        # else if admin button is clicked on
        elif request.form["submit"] == "Admin":
            # get the form input information and execute get method
            admin = jsonify(request.form).json
            admin = requests.get(
                'http://127.0.0.1:5000/api/login', params={'submit': admin['submit'], 'admin_username': admin['username'], 'admin_password': admin['password']}).json()

            # if the username and password, go back to login page and display warning message
            if admin == False:
                flash('The username or password is incorrect !')
                return render_template("login.html")

            # else, set the session and go to admin profile page
            else:
                session["admin_username"] = admin['username']
                session["admin_password"] = admin['password']
                return redirect(url_for("admin"))

    else:
        if "admin_username" in session:
            return redirect(url_for("admin"))
        elif "emp_username" in session:
            return redirect(url_for("employee"))
        return render_template("login.html")

# Route to logout
@app.route("/logout")
def logout():
    # pop out all the session
    session.pop("emp_id", None)
    session.pop("emp_username", None)
    session.pop("emp_password", None)
    session.pop("admin_username", None)
    session.pop("admin_password", None)
    return redirect(url_for("login"))


if __name__ == '__main__':
    # database_start()  # Uncomment and run if this is the first time to run this web apps
    app.run(debug=True)
