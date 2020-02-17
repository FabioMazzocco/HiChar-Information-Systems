'''=================================================================================================================='''
'''=================================================================================================================='''
'''================================================= Tables classes ================================================='''
'''=================================================================================================================='''
'''=================================================================================================================='''


class EmployeesTable(db.Model):
    __tablename__ = 'employeestable'
    id = db.Column(db.Integer, ForeignKey('userpass.id'), primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    hierarchy = db.Column(db.String(30), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    date_of_hiring = db.Column(db.DateTime, nullable=False)
    assigned_to_project = db.Column(db.Boolean, nullable=False)
    project_id = db.Column(db.Integer, ForeignKey('projects.id'), nullable=True)
    role = db.Column(db.String(30), nullable=True)
    id_rel = relationship('UserPass')
    project_rel = relationship('Projects')

    def __str__(self):
        return "Employee " + id + " (" + self.surname + " ," + self.name + ")"


class UserPass(db.Model):
    __tablename__ = 'userpass'
    id = db.Column(db.Integer, primary_key=True)
    hashed_psw = db.Column(db.String, nullable=False)


class Roles(db.Model):
    __tablename__ = 'roles'
    role = db.Column(db.String(30), primary_key=True)
    description = db.Column(db.Text, nullable=False)


class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.Integer, nullable=False)


class Skills(db.Model):
    __tablename__ = 'skills'
    name = db.Column(db.String(50), primary_key=True)
    soft_hard = db.Column(db.String(4), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __str__(self):
        print (self.name + " - " + self.soft_hard + " - " + self.category)

    def getCategory(self):
        return self.category+""


class PersonnelSkills(db.Model):
    __tablename__ = 'personnelskills'
    id = db.Column(db.Integer, ForeignKey('userpass.id'), primary_key=True)
    skill_name = db.Column(db.String(50), ForeignKey('skills.name'), primary_key=True)
    time = db.Column(db.Integer, nullable=True)
    id_rel = relationship('UserPass')
    skill_rel = relationship('Skills')


class RequestsProjects(db.Model):
    # __tablename__ = 'requestsprojects'
    id_project = db.Column(db.Integer, ForeignKey('projects.id'), primary_key=True)
    skill = db.Column(db.String(30), ForeignKey('skills.name'), primary_key=True)
    experience = db.Column(db.Integer, default=0)
    satisfied = db.Column(db.Boolean, default=False)
    project_rel = relationship('Projects')
    skill_rel = relationship('Skills')


class Courses(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    skill = db.Column(db.String(30), ForeignKey('skills.name'), nullable=False)
    level = db.Column(db.String(15), nullable=False)
    length = db.Column(db.Integer, nullable=False)
    skill_rel = relationship('Skills')