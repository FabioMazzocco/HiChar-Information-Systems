import binascii
import datetime
import hashlib
import os
import arrow
# import ctypes

from flask import Flask, render_template, request, redirect, session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from jinja2 import TemplateNotFound, Environment
from sqlalchemy.orm import load_only

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cecomp.db'
app.config['SECRET_KEY'] = "OCML3BRawWEUeaxcuKHLpw"
env = Environment(extensions=['jinja2_time.TimeExtension'])
db = SQLAlchemy(app)


'''=================================================================================================================='''
'''=================================================================================================================='''
'''================================================= Tables classes ================================================='''
'''=================================================================================================================='''
'''=================================================================================================================='''


class EmployeesTable(db.Model):
    # _tablename__ = 'employeestable'
    id = db.Column(db.Integer, primary_key=True)  # ForeignKey('userpass.id')
    username = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    hierarchy = db.Column(db.String(30), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    date_of_hiring = db.Column(db.DateTime, nullable=False)
    assigned_to_project = db.Column(db.Boolean, nullable=False)
    project_id = db.Column(db.Integer, nullable=True)  # ForeignKey('projects.id')
    role = db.Column(db.String(30), nullable=True)
    # id_rel = relationship('UserPass')
    # project_rel = relationship('Projects')

    def __str__(self):
        return "Employee " + id + " (" + self.surname + " ," + self.name + ")"


class UserPass(db.Model):
    # __tablename__ = 'userpass'
    id = db.Column(db.Integer, primary_key=True)
    hashed_psw = db.Column(db.String, nullable=False)


class Roles(db.Model):
    # __tablename__ = 'roles'
    role = db.Column(db.String(30), primary_key=True)
    description = db.Column(db.Text, nullable=False)


class Projects(db.Model):
    # __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.Integer, nullable=False)


class Skills(db.Model):
    # __tablename__ = 'skills'
    name = db.Column(db.String(50), primary_key=True)
    soft_hard = db.Column(db.String(4), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __str__(self):
        print (self.name + " - " + self.soft_hard + " - " + self.category)

    def getCategory(self):
        return self.category+""


class PersonnelSkills(db.Model):
    # __tablename__ = 'personnelskills'
    id = db.Column(db.Integer, primary_key=True)  # ForeignKey('userpass.id')
    skill_name = db.Column(db.String(50), primary_key=True)  # ForeignKey('skills.name')
    time = db.Column(db.Integer, nullable=True)
    # id_rel = relationship('UserPass')
    # skill_rel = relationship('Skills')


class RequestsProjects(db.Model):
    # __tablename__ = 'requestsprojects'
    id_project = db.Column(db.Integer, primary_key=True)  # ForeignKey('projects.id')
    skill = db.Column(db.String(30), primary_key=True)  # ForeignKey('skills.name')
    experience = db.Column(db.Integer, default=0)
    satisfied = db.Column(db.Boolean, default=False)
    # project_rel = relationship('Projects')
    # skill_rel = relationship('Skills')


class Courses(db.Model):
    # __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    skill = db.Column(db.String(30), nullable=False)  # ForeignKey('skills.name')
    level = db.Column(db.String(15), nullable=False)
    length = db.Column(db.Integer, nullable=False)
    # skill_rel = relationship('Skills')


'''=================================================================================================================='''
'''=================================================================================================================='''
'''=================================================== Web Server ==================================================='''
'''=================================================================================================================='''
'''=================================================================================================================='''
# Server initialization
if __name__ == '__main__':
    app.run()


# SOLVED: for future implementation it would be good to use SESSION or COOKIES (Json problem)
# Dictionary of logged user (key=id)
logged_users = {}


# Skills loading to cut the number of Server-DB connections (there is no problem of security)
skillsDict = {}
skillsDict.clear()
for skill in Skills.query.all():
    skillsDict[skill.name] = skill

# Projects loading to cut the number of Server-DB connections (there is no problem of security)
projectsDict = {}
for project in Projects.query.all():
    projectsDict[project.id] = project


@app.route('/', methods=["get", "post"])
def index():
    global logged_users, projectsDict
    if 'id' in session and session['id'] in logged_users:
        return render_template("index.html", user=logged_users.get(session['id']), utilities=utilities())
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
        session['id'] = employee.id
        logged_users[employee.id] = employee
        # print all_projects
        return render_template("index.html", user=employee, utilities=utilities())
    return redirect("/login", code=302)


@app.route('/login.html')
def redirect_to_login():
    return redirect('/login', code=302)


@app.route('/login')
def login():
    global logged_users
    if 'id' in session and session['id'] in logged_users:
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
    global logged_users
    # Removes the employee from the logged_users dictionary
    logged_users.pop(session['id'])
    # Removes the session
    session.pop('id', None)
    return redirect('/login', code=302)


@app.route('/all')
def all_employees():
    global logged_users
    if 'id' not in session or logged_users.get(session['id']) is None:
        return redirect('/login', code=302)
    logged_user = logged_users.get(session['id'])
    if logged_user.hierarchy == "Employee":
        return redirect("/", code=302)
    elif logged_user.hierarchy == "PM":
        return redirect("/employees", code=302)
    else:
        the_personnel = EmployeesTable.query.order_by(EmployeesTable.surname).all()
        return render_template("all_employees.html", user=logged_user, personnel=the_personnel,
                               utilities=utilities())


@app.route('/employees')
def only_employees():
    global logged_users
    if 'id' not in session or logged_users.get(session['id']) is None:
        return redirect('/login', code=302)
    logged_user = logged_users.get(session['id'])
    if logged_user.hierarchy == "Employee":
        return redirect("/", code=302)
    the_personnel = EmployeesTable.query.filter_by(hierarchy="Employee").order_by(EmployeesTable.surname).all()
    return render_template("only_employees.html", user=logged_user, personnel=the_personnel, utilities=utilities())


@app.route('/management')
def only_managers():
    global logged_users
    if 'id' not in session or logged_users.get(session['id']) is None:
        return redirect('/login', code=302)
    logged_user = logged_users.get(session['id'])
    if logged_user.hierarchy == "Employee" or logged_user.hierarchy == "PM":
        return redirect("/", code=302)
    the_personnel = EmployeesTable.query.filter_by(hierarchy="Manager").order_by(EmployeesTable.surname).all()
    return render_template("only_management.html", user=logged_user, personnel=the_personnel, utilities=utilities())


@app.route('/profile')
def profile():
    global logged_users
    if 'id' not in session or logged_users.get(session['id']) is None:
        return redirect('/login', code=302)
    logged_user = logged_users.get(session['id'])
    return render_template('profile.html', user=logged_user, profile=logged_user,
                           utilities=utilitiesPlus(logged_user.id), skills=getSkills(logged_user))


@app.route('/new_employee')
def new_employee():
    global logged_users
    if 'id' not in session or logged_users.get(session['id']) is None:
        return redirect('/login', code=302)
    logged_user = logged_users.get(session['id'])
    projectsList = Projects.query.all()
    rolesList = Roles.query.all()
    # print rolesList
    if logged_user.hierarchy == "HR":
        return render_template('new_employee.html', user=logged_user, utilities=utilities(), projects=projectsList,
                               roles=rolesList)
    else:
        return redirect('/', code=302)


@app.route('/result', methods=['GET', 'POST'])
def new_employee_result():
    global logged_users
    if 'id' not in session or logged_users.get(session['id']) is None:
        return redirect('/login', code=302)
    logged_user = logged_users.get(session['id'])
    if logged_user.hierarchy != "HR":
        return render_template('new_employee_result.html', user=logged_user, utilities=utilities(), success=0,
                               error_message="You were not qualified to add a new employee")
    # If there is something missing --> cannot add new employee --> message error
    missing = []
    for campo in request.form:
        if request.form.get(campo) == "":
            missing.append(campo.replace("newEmployee", "").lower())
    if len(missing) > 0:
        message = "Sorry, you missed some input fields:\n" + missing.__str__()
        return render_template('new_employee_result.html', user=logged_user, utilities=utilities(), success=0,
                               error_message=message)

    # If every input field is filled -->
    the_name = request.form["newEmployeeName"]
    the_surname = request.form["newEmployeeSurname"]
    the_username = request.form["newEmployeeUsername"]
    if len(EmployeesTable.query.filter_by(id=the_username).all()) > 0:
        return render_template('new_employee_result.html', user=logged_user, utilities=utilities(), success=0,
                               error_message="Sorry, there is already an existing employee with this username")
    the_password = request.form["newEmployeePassword"]
    the_id = request.form["newEmployeeID"]  # 6 digits
    if len(EmployeesTable.query.filter_by(id=the_id).all()) > 0:
        return render_template('new_employee_result.html', user=logged_user, utilities=utilities(), success=0,
                               error_message="Sorry, there is already an existing employee with this ID")
    the_email = request.form["newEmployeeUsername"] + "@" + request.form["newEmployeeEmail"]
    the_hierarchy = request.form["newEmployeeHierarchy"]  # First letter must be a capital letter. Possibilities: "Employee", "HR", "PM", "Manager"
    if len(the_hierarchy) > 8:
        the_hierarchy = the_hierarchy[0:2]
    the_date_of_birth = request.form["newEmployeeBirthday"]
    the_date_of_birth = datetime.strptime(the_date_of_birth, "%Y-%m-%d").date()
    the_date_of_hiring = request.form["newEmployeeHiringDate"]
    the_date_of_hiring = datetime.strptime(the_date_of_hiring, "%Y-%m-%d").date()
    the_assigned_to_project = int(request.form["newEmployeeAssigned"])   # Possibilities are: True or False (use False)
    if the_assigned_to_project == 0:
        the_assigned_to_project = False
    else:
        the_assigned_to_project = True
    the_project_id = request.form.get("newEmployeeProjectID", 0)  # If the employee is not assigned to any project, use 0
    the_role = request.form.get("newEmployeeRole", None)  # If the employee is not assigned to any project, use None
    if the_role == "-1":
        new_employee = EmployeesTable(id=the_id, username=the_username, name=the_name, surname=the_surname,
                                      email=the_email, hierarchy=the_hierarchy, date_of_birth=the_date_of_birth,
                                      date_of_hiring=the_date_of_hiring, assigned_to_project=the_assigned_to_project,
                                      project_id=the_project_id)
    else:
        new_employee = EmployeesTable(id=the_id, username=the_username, name=the_name, surname=the_surname,
                                      email=the_email, hierarchy=the_hierarchy, date_of_birth=the_date_of_birth,
                                      date_of_hiring=the_date_of_hiring, assigned_to_project=the_assigned_to_project,
                                      project_id=the_project_id, role=the_role)

    db.session.add(new_employee)

    user_pass = UserPass(id=the_id, hashed_psw=hash_password(the_password))
    db.session.add(user_pass)

    db.session.commit()
    return render_template('new_employee_result.html', user=logged_user, utilities=utilities(), success=1,
                           error_message="")


@app.route('/add_skills')
def add_skills():
    global logged_users
    if 'id' not in session or logged_users.get(session['id']) is None:
        return redirect('/login', code=302)
    logged_user = logged_users.get(session['id'])
    personnel_list = EmployeesTable.query.order_by("surname").all()
    for person in personnel_list:
        if person.id == logged_user.id:
            personnel_list.remove(person)
            break
    skills_list = Skills.query.order_by("name").all()
    categories_list = getCategories()
    hard_skills = {}
    soft_skills = {}
    for the_skill in skills_list:
        if the_skill.soft_hard == "Soft":
            if the_skill.getCategory() not in soft_skills:
                soft_skills[the_skill.getCategory()] = []
            soft_skills[the_skill.getCategory()].append(the_skill)
        else:
            if the_skill.getCategory() not in hard_skills:
                hard_skills[the_skill.getCategory()] = []
            hard_skills[the_skill.getCategory()].append(the_skill)
    if logged_user.hierarchy == "HR":
        return render_template('add_skills.html', user=logged_user, utilities=utilities(), personnel=personnel_list,
                               softSkills=soft_skills, hardSkills=hard_skills)
    else:
        return redirect('/', code=302)


@app.route('/add_skills_result', methods=['post'])
def add_skills_result():
    global logged_users
    if 'id' not in session or logged_users.get(session['id']) is None:
        return redirect('/login', code=302)
    logged_user = logged_users.get(session['id'])
    if logged_user.hierarchy != "HR":
        return render_template('add_skills_result.html', user=logged_user, utilities=utilities(), success=0,
                               error_message="You were not qualified to add skills to an employee")
    # If there is something missing --> cannot add new employee --> message error
    missing = []
    for campo in request.form:
        if request.form.get(campo) == "":
            missing.append(campo.lower())
    if len(missing) > 0:
        message = "Sorry, you missed some input fields:\n" + missing.__str__()
        return render_template('add_skills_result.html', user=logged_user, utilities=utilities(), success=0,
                               error_message=message)
    # print request.form
    employee = EmployeesTable.query.filter_by(id=request.form["employee"].split(" - ")[0]).first()
    if employee is None:
        return render_template('add_skills_result.html', user=logged_user, utilities=utilities(), success=0,
                               error_message="The selected employee does not exist")
    the_skill = Skills.query.filter_by(name=request.form["skill"]).first()
    if the_skill is None:
        return render_template('add_skills_result.html', user=logged_user, utilities=utilities(), success=0,
                               error_message="The selected skill does not exist")
    for person_skill in PersonnelSkills.query.filter_by(id=employee.id).all():
        if person_skill.skill_name == the_skill.name:
            return render_template('add_skills_result.html', user=logged_user, utilities=utilities(), success=0,
                                   error_message="The selected skill (" + the_skill.name +
                                   ") was already assigned to the employee (" + employee.surname + ", " +
                                   employee.name + ")")
    the_time = request.form.get("time")
    if the_time is None:
        return render_template('add_skills_result.html', user=logged_user, utilities=utilities(), success=0,
                                error_message="You need to insert a valid ampunt of time in months (integer)")
    try:
        the_time = int(the_time)
    except:
        return render_template('add_skills_result.html', user=logged_user, utilities=utilities(), success=0,
                               error_message="You need to insert a valid ampunt of time in months (integer)")
    personnel_skill = PersonnelSkills(id=employee.id, skill_name=the_skill.name, time=the_time)
    db.session.add(personnel_skill)
    db.session.commit()
    return render_template('add_skills_result.html', user=logged_user, utilities=utilities(), success=1,
                           error_message="")


@app.route('/projects')
def all_projects():
    global logged_users
    if 'id' not in session or logged_users.get(session['id']) is None:
        return redirect('/login', code=302)
    logged_user = logged_users.get(session['id'])
    if logged_user.hierarchy == "Employee":
        return redirect("/", code=302)
    else:
        the_projects = Projects.query.order_by(Projects.id).all()
        return render_template("projects.html", user=logged_user, projects=the_projects,
                               utilities=utilities())


@app.route('/training')
def training():
    global logged_users
    if 'id' not in session or logged_users.get(session['id']) is None:
        return redirect('/login', code=302)
    logged_user = logged_users.get(session['id'])
    the_courses = Courses.query.order_by("id").all()
    return render_template("training.html", user=logged_user, courses=the_courses,
                           utilities=utilities())


@app.route('/course/<int:course_id>')
def course(course_id):
    global logged_users
    if 'id' not in session or logged_users.get(session['id']) is None:
        return redirect('/login', code=302)
    logged_user = logged_users.get(session['id'])
    the_message = ""
    this_course = Courses.query.filter_by(id=course_id).first()
    if this_course is None:
        the_message = "The chosen course (" + str(course_id) + ") does not exist"
    else:
        the_message = "The chosen course (\"" + this_course.name + "\") is not available yet"
    return render_template("404.html", user=logged_user, utilities=utilities(), message=the_message)


@app.route('/requests')
def requests():
    global logged_users, skillsDict
    if 'id' not in session or logged_users.get(session['id']) is None:
        return redirect('/login', code=302)
    logged_user = logged_users.get(session['id'])
    the_requests = RequestsProjects.query.order_by("id_project").filter_by(satisfied=False).all()
    required_skills = {}
    for this_request in the_requests:
        if this_request.id_project not in required_skills:
            required_skills[this_request.id_project] = [this_request.id_project, 0, 0]
        the_skill = skillsDict.get(this_request.skill)
        if the_skill is None:
            print "skill not found: " + this_request.skill
            continue
        if the_skill.soft_hard == "Soft":
            required_skills[this_request.id_project][1] += 1
        else:
            required_skills[this_request.id_project][2] += 1
    everything_needed = {}
    for required_skill in required_skills:
        everything_needed[required_skill] = findBestThreeForProjectsRequests(required_skill)
    if logged_user.hierarchy == "PM":
        return render_template("request_for_personnel.html", user=logged_user, utilities=utilities(),
                               requests=the_requests, all_skills=skillsDict)
    elif logged_user.hierarchy == "HR":
        return render_template("HR_request_for_personnel.html", user=logged_user, utilities=utilities(),
                               requests=the_requests,  skills_requirement=required_skills, all_skills=skillsDict,
                               everything=everything_needed)
    else:
        return redirect("/", code=302)


@app.route('/allocate', methods=["post"])
def allocate():
    global logged_users
    if 'id' not in session or logged_users.get(session['id']) is None:
        return redirect('/login', code=302)
    logged_user = logged_users.get(session['id'])
    if logged_user.hierarchy != "HR":
        return redirect("/", code=302)
    the_requests = RequestsProjects.query.order_by("id_project").filter_by(satisfied=False).all()
    project = request.form.get("project_id")
    employee = request.form.get("employee_id")
    message = ""
    if project is None:
        message = "Ops, something went wrong, no project was selected"
        return render_template("allocate.html", user=logged_user, utilities=utilities(), success=0,
                               error_message=message)
    elif employee is None:
        message = "Ops, something went wrong, no employee was selected"
        return render_template("allocate.html", user=logged_user, utilities=utilities(), success=0,
                               error_message=message)
    the_success = 0
    project = int(project)
    employee = int(employee)
    for this_request in the_requests:
        if this_request.id_project == project:
            the_success = 1
            break
    if the_success == 0:
        message = "Sorry, the selected project does not require a new employee"
        return render_template("allocate.html", user=logged_user, utilities=utilities(), success=0,
                               error_message=message)
    employee = EmployeesTable.query.filter_by(id=employee).first()
    if employee.assigned_to_project:
        message = "Sorry, the employee has already been allocated previouosly"
        return render_template("allocate.html", user=logged_user, utilities=utilities(), success=0,
                               error_message=message)
    employee.assigned_to_project = True
    employee.project_id = project
    for this_request in RequestsProjects.query.filter_by(id_project=project).all():
        for this_skill in PersonnelSkills.query.filter_by(id=employee.id):
            if this_request.skill == this_skill.skill_name:
                this_request.satisfied = True
    db.session.commit()
    return render_template("allocate.html", user=logged_user, utilities=utilities(), success=1,
                           error_message="")


@app.route('/new_request_result', methods=["post"])
def new_request_result():
    global logged_users
    if 'id' not in session or logged_users.get(session['id']) is None:
        return redirect('/login', code=302)
    logged_user = logged_users.get(session['id'])
    if logged_user.hierarchy != "PM":
        return redirect("/", code=302)
    the_skill = request.form.get("skillSelection")
    if the_skill is None:
        return render_template('new_employee_result.html', user=logged_user, utilities=utilities(), success=0,
                               error_message="No skill was selected")
    the_skill = skillsDict.get(the_skill)
    if the_skill is None:
        return render_template('new_employee_result.html', user=logged_user, utilities=utilities(), success=0,
                               error_message="The selected skill does not exist")
    the_project = logged_user.project_id
    if len(RequestsProjects.query.filter_by(id_project=the_project, skill=the_skill.name).all()) != 0:
        return render_template('new_employee_result.html', user=logged_user, utilities=utilities(), success=0,
                               error_message="The selected skill has already been requested")
    the_time = request.form.get("time")
    if the_time is None:
        return render_template('new_employee_result.html', user=logged_user, utilities=utilities(), success=0,
                               error_message="The number of months of experience is mandatory")
    try:
        the_time = int(the_time)
    except:
        return render_template('new_employee_result.html', user=logged_user, utilities=utilities(), success=0,
                               error_message="The number of months of experience must be an integer")
    db.session.add(RequestsProjects(id_project=the_project, skill=the_skill.name, experience=the_time))
    db.session.commit()
    return render_template('new_employee_result.html', user=logged_user, utilities=utilities(), success=1,
                           error_message="")

# This route treat every case except the login and the index(home)
@app.route('/<string:pagename>', methods=['get', 'post'])
def user_dashboard(pagename):
    global logged_users
    pagename = pagename.split(".")[0]
    if 'id' not in session or logged_users.get(session['id']) is None:
        return redirect('/login', code=302)
    logged_user = logged_users.get(session['id'])
    all_users = EmployeesTable.query.all()

    # To see a profile (if pagename is an employee id)
    for employee in all_users:
        try:
            pagename = int(pagename)
        except ValueError:
            break
        if pagename == employee.id:
            if logged_user.hierarchy != "Employee":
                return render_template("profile.html", user=logged_user, profile=employee,
                                       utilities=utilitiesPlus(employee.id), skills=getSkills(employee))

    try:
        return render_template("" + pagename + ".html", user=logged_user, utilities=utilities())
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


'''=================================================================================================================='''
'''=================================================================================================================='''
'''=============================================== Useful functions ================================================='''
'''=================================================================================================================='''
'''=================================================================================================================='''


def utilities():
    now = datetime.utcnow()
    employeesNumber = len(EmployeesTable.query.all())
    skillsNumber = len(Skills.query.all())
    projectNumber = len(Projects.query.all())
    beginnerCoursesNumber = len(Courses.query.filter_by(level="Beginner").all())
    intermediateCoursesNumber = len(Courses.query.filter_by(level="Intermediate").all())
    expertCoursesNumber = len(Courses.query.filter_by(level="Expert").all())
    allCoursesNumber = beginnerCoursesNumber + intermediateCoursesNumber + expertCoursesNumber
    coursesType = [beginnerCoursesNumber, intermediateCoursesNumber, expertCoursesNumber, allCoursesNumber]
    the_projects = []
    for the_request in RequestsProjects.query.all():
        present = False
        for this_project in the_projects:
            if this_project["name"] == projectsDict.get(the_request.id_project).name:
                present = True
                break
        if not present:
            the_projects.append({"name": projectsDict.get(the_request.id_project).name,
                                 "satisfied": 0,
                                 "total": 0})
        for this_project in the_projects:
            if this_project["name"] == projectsDict.get(the_request.id_project).name:
                this_project["total"] += 1
                if the_request.satisfied:
                    this_project["satisfied"] += 1
    useful = [now, employeesNumber, skillsNumber, projectNumber, coursesType, the_projects]
    return useful


def utilitiesPlus(employee_id):
    global skillsDict
    useful = utilities()
    hard_skills = []
    soft_skills = []
    time = {}
    for skill_name in PersonnelSkills.query.filter_by(id=employee_id).all():
        this_skill = skillsDict.get(skill_name.skill_name)
        time[this_skill.name] = skill_name.time
        if this_skill.soft_hard == "Soft":
            soft_skills.append(this_skill)
        else:
            hard_skills.append(this_skill)
    useful.append(soft_skills)
    useful.append(hard_skills)
    useful.append(time)
    return useful


def getSkills(person):
    global skillsDict
    skillsPerson = PersonnelSkills.query.filter_by(id=person.id).all()
    # print skillsPerson
    softSkills = []
    hardSkills = []
    for one_skill in skillsPerson:
        one_skill = skillsDict[one_skill.skill_name]

        if one_skill.soft_hard == "Soft":
            softSkills.append(one_skill)
        else:
            hardSkills.append(one_skill)
    skillsPerson = {"Soft": softSkills, "Hard": hardSkills, "Number": (len(softSkills)+len(hardSkills))}
    return skillsPerson


def getCategories():
    global skillsDict
    category_dict = {}
    for the_skill in Skills.query.all():
        category_dict[the_skill.getCategory()] = the_skill.getCategory()
    return sorted(category_dict.keys())


def findBestThreeForProjectsRequests(project_id):
    global skillsDict
    requested_skills = []
    for request in RequestsProjects.query.filter_by(id_project=project_id, satisfied=False).all():
        requested_skills.append(skillsDict.get(request.skill))
    free_employees = EmployeesTable.query.filter_by(hierarchy="Employee", assigned_to_project=0).all()
    # List of dictionaries (first 3 positions)
    bests = [ {"employee": None, "score": 0, "hard": [], "soft": [], "skills_number": 0},
              {"employee": None, "score": 0, "hard": [], "soft": [], "skills_number": 0},
              {"employee": None, "score": 0, "hard": [], "soft": [], "skills_number": 0}]
    for employee in free_employees:
        skills = PersonnelSkills.query.filter_by(id=employee.id).all()
        score = 0
        # Algorithm: 1*boolean_have_the__hard_skill_or_not + 0.02*months_of_experience_with_the_skill +
        #              1*boolean_have_the__soft_skill_or_not
        this_employee = {"employee": employee, "score": 0, "hard": [], "soft": [], "skills_number": []}
        for the_skill in skills:
            for one_skill in requested_skills:
                if the_skill.skill_name == one_skill.name:
                    if one_skill.soft_hard == "Hard":
                        score += 1 + (0.02*the_skill.time)
                        this_employee["hard"].append(one_skill)
                    else:
                        score += 1
                        this_employee["soft"].append(one_skill)
        this_employee["score"] = score
        this_employee["skills_number"] = len(this_employee["hard"]) + len(this_employee["soft"])
        if score >= bests[2]["score"]:
            if score >= bests[0]["score"]:
                bests[2] = bests[1]
                if score == bests[0]["score"]:
                    order = case_even(bests[0], this_employee)
                    bests[1] = order[1]
                    bests[0] = order[0]
                else:
                    bests[1] = bests[0]
                    bests[0] = this_employee
            elif score >= bests[1]["score"]:
                if score == bests[1]["score"]:
                    order = case_even(bests[1], this_employee)
                    bests[2] = order[1]
                    bests[1] = order[0]
                else:
                    bests[2] = bests[1]
                    bests[1] = this_employee
            else:
                order = case_even(bests[2], this_employee)
                bests[2] = order[0]
    # print "BEST 3 for project " + str(project_id) + ": " + str(bests)
    return bests


def case_even(e1, e2):
    case1 = [e1, e2]
    case2 = [e2, e1]
    if e1["employee"] is None:
        return case2
    if len(e1["hard"]) >= len(e2["hard"]):
        if len(e1["hard"]) == len(e2["hard"]):
            if len(e1["soft"]) >= len(e2["soft"]):
                if len(e1["soft"]) == len(e2["soft"]):
                    if e1["employee"].date_of_birth >= e2["employee"].date_of_birth:
                        if e1["employee"].date_of_birth == e2["employee"].date_of_birth:
                            # Case hard1 = hard2 and soft1 = soft 2 and e1 same age of e2 and e1 hired first
                            if e1["employee"].date_of_hiring >= e2["employee"].date_of_hiring:
                                return case1
                            # Case hard1 = hard2 and soft1 = soft 2 and e1 same age of e2 and e2 hired first
                            else:
                                return case2
                        # Case hard1 = hard2 and soft1 = soft 2 and e1 older than e2
                        else:
                            return case2
                    # Case hard1 = hard2 and soft1 = soft 2 and e1 younger then e2
                    else:
                        return case1
                # Case hard1 = hard2 and soft1 > soft 2
                else:
                    return case1
            # Case hard1 = hard2 and soft1 < soft 2
            else:
                return case2
        # Case hard1 > hard2
        else:
            return case1
    # Case hard1 < hard2
    else:
        return case2