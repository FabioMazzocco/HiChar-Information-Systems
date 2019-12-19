from app import db, EmployeesTable, UserPass, Roles,  Projects, Skills, PersonnelSkills, RequestsProjects
from datetime import datetime
'''=================================================================================================================='''
'''=================================================================================================================='''
'''================================================ Adding Employees ================================================'''
'''=================================================================================================================='''
'''=================================================================================================================='''
# ADD 20 EMPLOYEES, 4 PROJECT MANAGERS, 2 MANAGERS
the_id = 000001   # 6 digits
the_username = "employee1"
the_name = "Fabio"
the_surname = "Fabio"
the_email = "employee1@studenti.polito.it"
the_hierarchy = "Employee"  # First letter must be a capital letter. Possibilities: "Employee", "HR", "PM", "Manager"
the_date_of_birth = datetime.date(1997, 12, 13)
the_date_of_hiring = datetime.date(2019, 12, 7)
the_assigned_to_project = False   # Possibilities are: True or False (use False)
the_project_id = 0     # If the employee is not assigned to any project, use 0
the_role = None   # If the employee is not assigned to any project, use None

new_employee = EmployeesTable(id=the_id, username=the_username, name=the_name, surname=the_surname,\
                              email=the_email, hierarchy=the_hierarchy, date_of_birth=the_date_of_birth,\
                              date_of_hiring=the_date_of_hiring, assigned_to_project=the_assigned_to_project, \
                              project_id=the_project_id, role=the_role)

db.session.add(new_employee)
db.session.commit()
for employee in EmployeesTable.query.all():
    print(employee.__dict__)


'''=================================================================================================================='''
'''=================================================================================================================='''
'''========================================== Adding password to employees =========================================='''
'''=================================================================================================================='''
'''=================================================================================================================='''
# FOR EVERY PERSON CREATED BEFORE, PUT THE ID AND THE PASSWORD (THE PASSWORD IS THE ID)
# the_id = 222222
# the_password = "222222"   # Same as ID but within "...."

# user_pass = UserPass(id=the_id, hashed_psw=hash_password(the_password))
# db.session.add(user_pass)
# db.session.commit()

# for record in UserPass.query.all():
#    print(record.__dict__)


'''=================================================================================================================='''
'''=================================================================================================================='''
'''================================================== Adding skills ================================================='''
'''=================================================================================================================='''
'''=================================================================================================================='''
# ADD SOFT SKILLS FROM https://resumegenius.com/blog/resume-help/soft-skills (ALL SKILL UNTIL CATEGORY 7 ADDED)
# ADD HARD SKILLS (10-15 THAT YOU WANT)

# the_type = "Soft"    # Please mind the capital letter at the beginning. Possibilities: "Soft" or "Hard"
# the_category = "Work Ethic"
# the_name = "Time-management"
# the_description = "The process of organizing and planning how to divide your time between specific activities"

# skill = Skills(soft_hard=the_type, category=the_category, name=the_name, description=the_description)
# db.session.add(skill)
# db.session.commit()
# print(len(Skills.query.all()))


'''=================================================================================================================='''
'''=================================================================================================================='''
'''================================================== Adding projects ==============================================='''
'''=================================================================================================================='''
'''=================================================================================================================='''
# ADD 5 PROJECTS BASED ON CECOMP HISTORY (SEE SAMPLE BELOW)

# the_project_id = 1
# the_name = "BlueCar"
# the_description = "Electric cars for car sharing all over the world"
# the_duration = 5*12   # The duration is in months --> 5 years = 5 times 12 months = 60

# project = Projects(id=the_project_id, name=the_name, description=the_description, duration=the_duration)
# db.session.add(project)
# db.session.commit()
# print(Projects.query.all())

'''=================================================================================================================='''
'''=================================================================================================================='''
'''============================================== Adding projects-skills ============================================'''
'''=================================================================================================================='''
'''=================================================================================================================='''
# FOR EACH PROJECT CHOOSE 6 SKILLS REQUIRED (3 SOFT SKILLS, 3 HARD SKILLS)

# the_project_id = 1
# the_skill = ""
# requested = RequestsProjects(id_project=the_project_id, skill=the_skill)
# db.session.add(requested)
# db.session.commit()
# print(RequestsProjects.query.all())
