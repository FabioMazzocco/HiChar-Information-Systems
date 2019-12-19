class User:

    def __init__(self, username, password, role, seniority_years):
        self.username = username
        self.password = password
        self.role = role
        self.softSkills = []
        self.hardSkills = []
        self.seniority_years = seniority_years

    def __str__(self):
        return "{}, {}".format(self.username, self.role)