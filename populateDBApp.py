from flask import session
from app import db, EmployeesTable, UserPass, Roles,  Projects, Skills, PersonnelSkills, RequestsProjects, \
    hash_password, Courses
from datetime import datetime


'''=================================================================================================================='''
'''=================================================================================================================='''
'''================================================ Adding Employees ================================================'''
'''=================================================================================================================='''
'''=================================================================================================================='''
"""f = open("toBeAdded.txt", "r")
for l in f.readlines():
    stuff = []
    for a in l.split(","):
        a = a.replace("'", "")
        try:
            a = int(a)
        except:
            if a == "NULL":
                a = None
            a = a
        stuff.append(a)
    del stuff[-1]
    stuff.append(None)
    print stuff
    if stuff[9] is None:
        new_employee = EmployeesTable(id=stuff[0], username=stuff[1], name=stuff[2], surname=stuff[3],
                                      email=stuff[4], hierarchy=stuff[5], date_of_birth=datetime.strptime(stuff[6],
                                                                                                          "%d/%m/%Y"),
                                      date_of_hiring=datetime.strptime(stuff[7], "%Y/%m/%d"),
                                      assigned_to_project=stuff[8])
    elif stuff[10] is None:
        new_employee = EmployeesTable(id=stuff[0], username=stuff[1], name=stuff[2], surname=stuff[3],
                                      email=stuff[4], hierarchy=stuff[5], date_of_birth=datetime.strptime(stuff[6],
                                                                                                          "%d/%m/%Y"),
                                      date_of_hiring=datetime.strptime(stuff[7], "%Y/%m/%d"),
                                      assigned_to_project=stuff[8],
                                      project_id=stuff[9])
    else:
        new_employee = EmployeesTable(id=stuff[0], username=stuff[1], name=stuff[2], surname=stuff[3],
                                      email=stuff[4], hierarchy=stuff[5], date_of_birth=datetime.strptime(stuff[6],
                                                                                                      "%d/%m/%Y"),
                                      date_of_hiring=datetime.strptime(stuff[7], "%Y/%m/%d"), assigned_to_project=stuff[8],
                                      project_id=stuff[9], role=stuff[10])
    db.session.add(new_employee)
    db.session.commit()"""

# the_id = 000003   # 6 digits
# the_username = "employee03"
# the_name = "Zahra"
# the_surname = "Gm"
# the_email = "employee03@studenti.polito.it"
# the_hierarchy = "Employee"  # First letter must be a capital letter. Possibilities: "Employee", "HR", "PM", "Manager"
# the_date_of_birth = datetime(1997, 12, 13)
# the_date_of_hiring = datetime(2019, 12, 7)
# the_assigned_to_project = False   # Possibilities are: True or False (use False)
# the_project_id = 0     # If the employee is not assigned to any project, use 0
# the_role = None   # If the employee is not assigned to any project, use None

# new_employee = EmployeesTable(id=the_id, username=the_username, name=the_name, surname=the_surname,
#                              email=the_email, hierarchy=the_hierarchy, date_of_birth=the_date_of_birth,
#                             date_of_hiring=the_date_of_hiring, assigned_to_project=the_assigned_to_project,
#                             project_id=the_project_id, role=the_role)

# db.session.add(new_employee)
# db.session.commit()
# for employee in EmployeesTable.query.all():
#    print(employee.__dict__)


'''=================================================================================================================='''
'''=================================================================================================================='''
'''========================================== Adding password to employees =========================================='''
'''=================================================================================================================='''
'''=================================================================================================================='''
"""already_present = []
for user in UserPass.query.all():
    already_present.append(user.id)
for user in EmployeesTable.query.all():
    if user.id in already_present:
        print "Found one"
        continue
    the_id = user.id
    the_password = str(user.id)   # Same as ID but within "...."

    user_pass = UserPass(id=the_id, hashed_psw=hash_password(the_password))
    db.session.add(user_pass)
db.session.commit()"""
"""db.session.add(UserPass(id=int("080301"), hashed_psw=hash_password("080301")))
db.session.commit()"""
# for record in UserPass.query.all():
#    print(record.__dict__)


'''=================================================================================================================='''
'''=================================================================================================================='''
'''================================================== Adding skills ================================================='''
'''=================================================================================================================='''
'''=================================================================================================================='''
"""already_present = Skills.query.all()
f = open("toBeAdded.txt", "r")
for l in f.readlines():
    stuff = []
    print l
    for a in l.split(";"):
        if a == "NULL":
            a = None
            stuff.append(a)
        else:
            stuff.append(a.replace("'", ""))
    del stuff[-1]
    present = False
    for skill in already_present:
        if skill.name == stuff[0]:
            present = True
            break
    if present:
        continue
    skill = Skills(soft_hard=stuff[1], category=stuff[2], name=stuff[0], description=stuff[3])
    toBePrinted = ""
    for x in range(4):
        toBePrinted += str(x) + " - " + stuff[x] + "\n"
    print toBePrinted
    db.session.add(skill)

db.session.commit()"""


"""the_type = "Soft"    # Please mind the capital letter at the beginning. Possibilities: "Soft" or "Hard"
the_category = "Interpersonal Skills"
the_name = "Humor"
the_description = "The quality of being amusing or comic"

skill = Skills(soft_hard=the_type, category=the_category, name=the_name, description=the_description)
db.session.add(skill)
db.session.commit()
print(len(Skills.query.all()))"""


'''=================================================================================================================='''
'''=================================================================================================================='''
'''================================================== Adding projects ==============================================='''
'''=================================================================================================================='''
'''=================================================================================================================='''
# the_project_id = 4
# the_name = "McLaren"
# the_description = "Production of a sport car for McLaren"
# the_duration = 2.5*12   # The duration is in months --> 5 years = 5 times 12 months = 60

#  project = Projects(id=the_project_id, name=the_name, description=the_description, duration=the_duration)
#  db.session.add(project)
#  db.session.commit()
# print(Projects.query.all())

'''=================================================================================================================='''
'''=================================================================================================================='''
'''============================================== Adding projects-skills ============================================'''
'''=================================================================================================================='''
'''=================================================================================================================='''
# FOR EACH PROJECT CHOOSE 6 SKILLS REQUIRED (4 SOFT SKILLS, 4 HARD SKILLS)
f = open("toBeAdded.txt", "r")
"""for l in f.readlines():
    a = l.split(";")
    project_number = int(a[0])
    the_skill = a[1]
    the_time = int(a[2])
    the_satisfied = False
    db.session.add(RequestsProjects(id_project=project_number, skill=the_skill, experience=the_time, satisfied=False))
db.session.commit()"""

"""the_project_id = 1
the_skill = "Project management software"  # First letter must be a capital letter
requested = RequestsProjects(id_project=the_project_id, skill=the_skill, experience=12, satisfied=False)
db.session.add(requested)
db.session.commit()
print(RequestsProjects.query.all())"""


'''=================================================================================================================='''
'''=================================================================================================================='''
'''============================================== Adding skills to employees ========================================'''
'''=================================================================================================================='''
'''=================================================================================================================='''
"""f = open("toBeAdded.txt", "r")
already_present = PersonnelSkills.query.all()
for l in f.readlines():
    a = l.split(";")
    the_id = int(a[0])
    the_skill = a[1]
    the_duration = int((a[2].split("\n"))[0])
    toBeAdded = PersonnelSkills(id=the_id, skill_name=the_skill, time=the_duration)
    # print str(the_id) + " - " + the_skill + " - " + str(the_duration)
    present = False
    for already_present_skill in already_present:
        if already_present_skill.id == the_id and already_present_skill.skill_name == the_skill:
            present = True
            break
    if present:
        continue
    db.session.add(toBeAdded)
db.session.commit()"""


'''=================================================================================================================='''
'''=================================================================================================================='''
'''==================================================== Adding courses =============================================='''
'''=================================================================================================================='''
'''=================================================================================================================='''
"""the_id = 0
the_name = "Learn Project Management"
the_skill = "Project management"
the_level = "Beginner"
the_length = 100"""

f = open("toBeAdded.txt", "r")
for l in f.readlines():
    a = l.split(";")
    print a
    the_id = int(a[0])
    the_name = a[1]
    the_skill = a[2]
    the_level = a[3]
    the_length = int(a[4])
    db.session.add(Courses(id=the_id, name=the_name, skill=the_skill, level=the_level, length=the_length))
    db.session.commit()
print Courses.query.all()
