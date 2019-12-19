import binascii
import datetime
import hashlib
import os
# import ctypes

from flask import Flask, render_template, request, redirect, session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from jinja2 import TemplateNotFound

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cecomp.db'
app.config['SECRET_KEY'] = "OCML3BRawWEUeaxcuKHLpw"
db = SQLAlchemy(app)
logged_user = None

'''=================================================================================================================='''
'''=================================================================================================================='''
'''================================================= Tables classes ================================================='''
'''=================================================================================================================='''
'''=================================================================================================================='''


class EmployeesTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    hierarchy = db.Column(db.String(30), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    date_of_hiring = db.Column(db.DateTime, nullable=False)
    assigned_to_project = db.Column(db.Boolean, nullable=False)
    project_id = db.Column(db.Integer, nullable=True)
    role = db.Column(db.String(30), nullable=True)

    def __str__(self):
        return "Employee " + id + " (" + self.surname + " ," + self.name + ")"


class UserPass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hashed_psw = db.Column(db.String, nullable=False)


class Roles(db.Model):
    role = db.Column(db.String(30), primary_key=True)
    description = db.Column(db.Text, nullable=False)


class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.Integer, nullable=False)


class Skills(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    soft_hard = db.Column(db.String(4), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __str__(self):
        print (self.name + " - " + self.soft_hard + " - " + self.category)


class PersonnelSkills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(50), primary_key=True)
    time = db.Column(db.Integer, nullable=True)


class RequestsProjects(db.Model):
    id_project = db.Column(db.Integer, primary_key=True)
    skill = db.Column(db.String(30), primary_key=True)
    experience = db.Column(db.Integer, default=0)


'''=================================================================================================================='''
'''=================================================================================================================='''
'''=================================================== Web Server ==================================================='''
'''=================================================================================================================='''
'''=================================================================================================================='''
if __name__ == '__main__':
    app.run()


@app.route('/', methods=["get", "post"])
def index():
    global logged_user
    if logged_user is not None:
        return render_template("index.html", user=logged_user)
    if request.method == 'POST':
        username = request.form['exampleInputEmail']
        username = username.split("@")[0]
        password = request.form['exampleInputPassword']
        # Check on username and password
        employee = EmployeesTable.query.filter_by(username=username).first()
        if employee is None:
            return redirect("/login", code=302)
        user = UserPass.query.filter_by(id=employee.id).first()
        # if the password is wrong
        if not verify_password(user.hashed_psw, password):
            return redirect("/login", code=302)
        logged_user = employee  # session['user'] = employee
        return render_template("index.html", user=logged_user)  # session['user'])
    return redirect("/login", code=302)


@app.route('/login.html')
def redirect_to_login():
    return redirect('/login', code=302)


@app.route('/login')
def login():
    global logged_user
    if logged_user is not None:
        return redirect("/", code=302)
    return render_template("login.html")


@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot-password.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/logout')
def logout():
    global logged_user
    logged_user = None
    return redirect('/login', code=302)


@app.route('/requests')
def requests():
    global logged_user
    if logged_user is None:
        return redirect('index', code=302)
    elif logged_user.hierarchy == "PM":
        return render_template("request_for_personnel.html", user=logged_user)
    else:
        return render_template("HR_request_for_personnel.html", user=logged_user)


@app.route('/all')
def all_employees():
    global logged_user
    if logged_user is None:
        return redirect('/', code=302)
    current_time = datetime.now()
    the_personnel = EmployeesTable.query.order_by(EmployeesTable.surname).all()
    return render_template("all_employees.html", user=logged_user, personnel=the_personnel, now=current_time)


@app.route('/employees')
def only_employees():
    global logged_user
    if logged_user is None:
        return redirect('/', code=302)
    current_time = datetime.now()
    the_personnel = EmployeesTable.query.filter_by(hierarchy="Employee").order_by(EmployeesTable.surname).all()
    return render_template("only_employees.html", user=logged_user, personnel=the_personnel, now=current_time)


@app.route('/management')
def only_managers():
    global logged_user
    if logged_user is None:
        return redirect('/', code=302)
    current_time = datetime.now()
    the_personnel = EmployeesTable.query.filter_by(hierarchy="Manager").order_by(EmployeesTable.surname).all()
    return render_template("only_management.html", user=logged_user, personnel=the_personnel, now=current_time)


# This route treat every case except the login and the index(home)
@app.route('/<string:pagename>', methods=['get', 'post'])
def user_dashboard(pagename):
    global logged_user
    pagename = pagename.split(".")[0]
    if logged_user is None:
        return redirect("/login", code=302)
    try:
        return render_template("" + pagename + ".html", user=logged_user)
    except TemplateNotFound as t:
        return redirect("/", code=302)


'''=================================================================================================================='''
'''=================================================================================================================='''
'''========================================== Password saving/retrieving ============================================'''
'''=================================================================================================================='''
'''=================================================================================================================='''


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password
