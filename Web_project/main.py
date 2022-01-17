from crypt import methods
import sqlite3
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_cors import CORS

def database_connection():
    con = sqlite3.connect('database.db')
    return con


def add_emp(emp_username, emp_password, emp_name, gender, academic, email, emp_address):
    add_employee = []
    try:
        con = database_connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM employee_info WHERE Username = ? ",
                       (emp_username,))
        i = cursor.fetchone()
        # convert row object to dictionary

        if not i:
            cursor.execute("INSERT INTO employee_info ( Username, Password, employee_name, gender, Academic_qualification, email, address ) VALUES(?, ?, ?, ?, ?, ?, ?)",
                           (emp_username, emp_password, emp_name, gender, academic, email, emp_address))

        else:
            return False


        con.commit()
        add_employee = get_emp_by_id(cursor.lastrowid)
        print(add_employee)
    except:
        con().rollback()

    finally:
        con.close()

    return add_employee


def get_emp():
    employees = []
    try:
        con = database_connection()
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("SELECT * FROM employee_info")
        all = cursor.fetchall()

        # convert row objects to dictionary
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

    except:
        employees = []

    finally:
        con.close()

    return employees


def get_emp_by_id(emp_id):
    emp = {}
    try:
        con = database_connection()
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("SELECT * FROM employee_info WHERE employee_id = ?",
                       (emp_id,))
        i = cursor.fetchone()

        # convert row object to dictionary
        emp = {}
        emp["emp_id"] = i["employee_id"]
        emp["name"] = i["employee_name"]
        emp["gender"] = i["gender"]
        emp["email"] = i["email"]
        emp["address"] = i["address"]
        emp["academic"] = i["Academic_qualification"]
        emp["username"] = i["Username"]
        emp["password"] = i["Password"]
    except:
        emp = {}

    finally:
        con.close()

    return emp


def update_emp(emp_name, gender, email, address, academic, emp_password, emp_id):
    update_emp = {}
    try:
        con = database_connection()
        cursor = con.cursor()
        cursor.execute("UPDATE employee_info SET employee_name= ?, gender= ?, email= ?, address= ?,Academic_qualification= ?, Password =? WHERE employee_id=?",
                       (emp_name, gender, email, address, academic,  emp_password, emp_id))
        con.commit()
        #return the employee
        update_emp = get_emp_by_id(emp_id)

    except:
        con.rollback()
        update_emp = {}
    finally:
        con.close()

    return update_emp


def delete_emp(emp_id):
    message = {}
    try:
        con = database_connection()
        con.execute("DELETE from employee_info WHERE employee_id = ?",
                    (emp_id,))
        con.commit()
        message["status"] = "Employee is deleted successfully"
    except:
        con.rollback()
        message["status"] = "Cannot delete employee"
    finally:
        con.close()

    return message

def login_emp(emp_username, emp_password):
    emp = {}
    try:
        con = database_connection()
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("SELECT * FROM employee_info WHERE Username = ? AND Password = ?",
                       (emp_username, emp_password,))
        i = cursor.fetchone()

        # convert row object to dictionary
        emp = {}
        emp["emp_id"] = i["employee_id"]
        emp["name"] = i["employee_name"]
        emp["gender"] = i["gender"]
        emp["email"] = i["email"]
        emp["address"] = i["address"]
        emp["academic"] = i["Academic_qualification"]
        emp["username"] = i["Username"]
        emp["password"] = i["Password"]

    except:
        return False

    finally:
        con.close()

    return emp

def login_admin(admin_username, admin_password):
    admin = {}
    try:
        con = database_connection()
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("SELECT * FROM admin_auth WHERE Username = ? AND Password = ?",
                       (admin_username, admin_password,))
        i = cursor.fetchone()

        admin = {}
        admin["username"] = i["Username"]
        admin["password"] = i["Password"]

    except:
        return False

    finally:
        con.close()

    return admin


def add_admin(admin_username, admin_password):
    try:
        con = database_connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM admin_auth WHERE Username = ? ",
                       (admin_username,))
        i = cursor.fetchone()
        # convert row object to dictionary

        if not i:
            cursor.execute("INSERT INTO admin_auth ( Username, Password) VALUES(?, ?)",
                           (admin_username, admin_password))
        else:
            return False

        con.commit()

        admin = {}
        admin["username"] = admin_username
        admin["password"] = admin_password

    except:
        con().rollback()

    finally:
        con.close()

    return admin

app = Flask(__name__)
app.secret_key = "Hello"

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/signup_emp/", methods=["POST", "GET"])
def signup_emp():
    if request.method == "POST":
        session.permanent = True  # <--- makes the permanent session
        emp_username = request.form["emp_username"]
        emp_password = request.form["emp_password"]
        emp_name = request.form["emp_name"]
        gender = request.form["gender"]
        academic = request.form["academic"]
        if academic != "NONE":
            email = request.form["email"]
            emp_address = request.form["emp_address"]
            emp = add_emp(emp_username, emp_password, emp_name, gender, academic, email, emp_address)
            if emp == False:
                flash('The username is existed!')
                return render_template("signup_emp.html")
            else:
                session["emp_username"] = emp_username
                session["emp_password"] = emp_password
                emp_id = emp['emp_id']
                session["emp_id"] = emp_id
                return redirect(url_for("employee"))
        else:
            flash('The Academic_qualification field cannot be empty !')
            return render_template("signup_emp.html")

    else:
        return render_template("signup_emp.html")


@app.route("/signup_admin", methods=["POST", "GET"])
def signup_admin():
    if request.method == "POST":
        session.permanent = True  # <--- makes the permanent session
        admin_username = request.form["admin_username"]
        admin_password = request.form["admin_password"]
        admin = add_admin(admin_username, admin_password)
        if admin == False:
            flash('The username is existed!')
            return render_template("signup_admin.html")
        else:
            session["admin_username"] = admin_username
            session["admin_password"] = admin_password
            return redirect(url_for("admin"))
    else:
        return render_template("signup_admin.html")

@app.route("/employee")
def employee():
    if "emp_username" in session:
        emp_id = session["emp_id"]
        emp = get_emp_by_id(emp_id)
        emp_name = emp["name"]
        gender = emp["gender"]
        academic = emp["academic"]
        email = emp["email"]
        emp_address = emp["address"]
        emp_username = emp["username"]
        emp_password = emp["password"]
        return render_template("employee.html", emp_id = emp_id, emp_name = emp_name, gender = gender, academic = academic, email = email, emp_address = emp_address, emp_username = emp_username, emp_password = emp_password)

    elif "admin_username" in session:
        emp_id = session["emp_id"]
        emp = get_emp_by_id(emp_id)
        if emp != {}:
            emp_name = emp["name"]
            gender = emp["gender"]
            academic = emp["academic"]
            email = emp["email"]
            emp_address = emp["address"]
            emp_username = emp["username"]
            emp_password = emp["password"]
            return render_template("employee.html", emp_id = emp_id, emp_name = emp_name, gender = gender, academic = academic, email = email, emp_address = emp_address, emp_username = emp_username, emp_password = emp_password)
        else:
            flash('The employee ID does not exist !')
            return redirect(url_for("employee_list"))
    else:
        return redirect(url_for("login"))


@app.route('/updateEmployee', methods=["POST", "GET"])
def updateEmployee():
    if request.method == "POST":
        emp_id = session["emp_id"]
        emp_password = request.form["emp_password"]
        emp_name = request.form["emp_name"]
        gender = request.form["gender"]
        academic = request.form["academic"]
        email = request.form["email"]
        address = request.form["emp_address"]
        emp = update_emp(emp_name, gender, email, address,
                         academic, emp_password, emp_id)
        if emp != {}:
            flash('The employee is updated !')
        else:
            flash('The employee cannot be updated !')
        return redirect(url_for("employee"))

    else:
        emp_id = session["emp_id"]
        emp = get_emp_by_id(emp_id)
        emp_id = emp["emp_id"]
        emp_username = emp["username"]
        emp_password = emp["password"]
        emp_name = emp["name"]
        gender = emp["gender"]
        academic = emp["academic"]
        email = emp["email"]
        emp_address = emp["address"]
        return render_template("update.html", emp_id=emp_id, emp_name=emp_name, gender=gender, academic=academic, email=email, emp_address=emp_address, emp_username=emp_username, emp_password=emp_password)

@app.route("/admin")
def admin():
    if "admin_username" in session:
        admin_username = session["admin_username"]
        admin_password = session["admin_password"]
        return render_template("admin.html", admin=admin_username,password = admin_password )
    else:
        return redirect(url_for("login"))


@app.route('/employeeList')
def employee_list():
    emp = get_emp()
    return render_template("employee_list.html", emp=emp)


@app.route('/searchEmployee', methods=["POST"])
def searchEmployee():
    emp_id = request.form["emp_id"]
    session["emp_id"] = emp_id
    return redirect(url_for("employee"))


@app.route("/addEmployee", methods=["POST", "GET"])
def add_employee():
    if request.method == "POST":
        emp_username = request.form["emp_username"]
        emp_password = request.form["emp_password"]
        emp_name = request.form["emp_name"]
        gender = request.form["gender"]
        academic = request.form["academic"]
        email = request.form["email"]
        emp_address = request.form["emp_address"]
        if academic != "NONE":
            emp = add_emp(emp_username, emp_password, emp_name,
                      gender, academic, email, emp_address)
            if emp == False:
                flash('The username is existed!')
                return render_template("add_emp.html")
            else:
                emp_id = emp['emp_id']
                session["emp_id"] = emp_id
                flash('An employee is added !')
                return redirect(url_for("employee"))
        else:
            flash('The Academic_qualification field cannot be empty !')
            return render_template("add_emp.html")
    else:
        return render_template("add_emp.html")


@app.route('/deleteEmployee', methods=["POST"])
def deleteEmployee():
    emp_id = request.form["emp_id"]
    session.pop("emp_id", None)
    message = delete_emp(emp_id)
    message = message["status"]
    flash(message)
    return redirect(url_for("employee_list"))



@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True  # <--- makes the permanent session
        if request.form["submit"] == "Employee":
            emp_username = request.form["username"]
            emp_password = request.form["password"]
            emp = login_emp(emp_username, emp_password)
            if emp == False:
                flash('The username or password is incorrect !')
                return render_template("login.html")
            else:
                session["emp_id"] = emp['emp_id']
                session["emp_username"] = emp_username
                return redirect(url_for("employee"))

        elif request.form["submit"] == "Admin":
            admin_username = request.form["username"]
            admin_password = request.form["password"]
            admin = login_admin(admin_username, admin_password)
            if admin == False:
                flash('The username or password is incorrect !')
                return render_template("login.html")
            else:
                session["admin_username"] = admin_username
                session["admin_password"] = admin_password
                return redirect(url_for("admin"))

    else:
        if "admin_username" in session:
            return redirect(url_for("admin"))
        elif "emp_username" in session:
            return redirect(url_for("employee"))
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("emp_id", None)
    session.pop("emp_username", None)
    session.pop("emp_password", None)
    session.pop("admin_username", None)
    session.pop("admin_password", None)
    return redirect(url_for("login"))


app.run(debug=True)
