# Flask Web Application using SQLite

A full-stack employee management web application built with Flask, Bootstrap, and SQLite. Supports two user roles — Admin and Employee — with session-based authentication.

Two versions are available:
- `Web_project/` — standard Flask version
- `Web_project/with REST API/` — extended version with a REST API layer using Flask-RESTful

---

## Features

### Admin
- Sign up and log in as admin
- View admin profile
- Add a new employee
- Update any employee's information
- Search for an employee by ID
- Delete an employee
- View all employees in a list

### Employee
- Sign up and log in as employee
- View own profile
- Update own profile

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| Frontend | HTML, Bootstrap |
| Auth | Flask session |
| REST API (v2) | Flask-RESTful, requests |

---

## Project Structure

```
Flask-Web-Application-using-SQLite/
├── Web_project/                   # Standard Flask version
│   ├── templates/                 # HTML templates (Jinja2)
│   │   ├── index.html             # Home page
│   │   ├── login.html             # Login page
│   │   ├── signup.html            # Signup selection page
│   │   ├── signup_emp.html        # Employee signup
│   │   ├── signup_admin.html      # Admin signup
│   │   ├── employee.html          # Employee profile
│   │   ├── admin.html             # Admin profile
│   │   ├── employee_list.html     # All employees list
│   │   ├── add_emp.html           # Add employee form
│   │   ├── update.html            # Update employee form
│   │   └── bootstrap.html         # Bootstrap base template
│   ├── main.py                    # Flask app + routes + DB functions
│   ├── db.py                      # Database initialisation script
│   └── requirements.txt           # Python dependencies
│
├── Web_project/with REST API/     # REST API version
│   ├── templates/                 # Same HTML templates
│   ├── CST330_project.py          # Flask app + REST API endpoints
│   └── requirements.txt           # Python dependencies
│
├── .gitignore
└── README.md
```

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/Flask-Web-Application-using-SQLite.git
cd Flask-Web-Application-using-SQLite
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

For the standard version:
```bash
cd Web_project
pip install -r requirements.txt
```

For the REST API version:
```bash
cd "Web_project/with REST API"
pip install -r requirements.txt
```

### 4. Initialise the database

Run this **once** before the first launch to create the SQLite tables.
This also creates a default admin account (`username: admin`, `password: admin`).

For the standard version:
```bash
cd Web_project
python db.py
```

For the REST API version, uncomment `database_start()` in `CST330_project.py` and run once:
```python
# In CST330_project.py, uncomment this line at the bottom:
database_start()
```

### 5. Run the application

For the standard version:
```bash
cd Web_project
python main.py
```

For the REST API version:
```bash
cd "Web_project/with REST API"
python CST330_project.py
```

Then open your browser and go to:
```
http://127.0.0.1:5000
```

---

## Usage

### Login as Admin
- Use the default admin account: `username: admin`, `password: admin`
- Or sign up a new admin account via the Sign Up page

### Login as Employee
- Sign up as a new employee via the Sign Up page
- Log in with your registered username and password

---

## REST API Endpoints (v2 only)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/emp_all` | Get all employees |
| POST | `/add_emp` | Add a new employee |
| GET | `/emp/get?emp_id=<id>` | Get employee by ID |
| PUT | `/emp/put` | Update an employee |
| DELETE | `/emp/delete?emp_id=<id>` | Delete an employee |
| POST | `/add_admin` | Add a new admin |
| GET | `/api/login` | Login for admin or employee |

---

## Known Limitations

- Passwords are stored in **plaintext** — no hashing is applied. This is a learning project and not intended for production use.
- The `secret_key` in `main.py` is hardcoded as `"Hello"` — should be replaced with a secure random key for any real deployment.
- No HTTPS — runs on HTTP locally only.

---
