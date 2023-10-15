
# import SQLALchemy
from App import db
from flask import request, redirect

# Define class Department
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deptName = db.Column(db.String(100))
    job_dept = db.Column(db.String(100)) 
    Salary = db.Column(db.String(100))
    Description = db.Column(db.String(100))
    date_registered = db.Column(db.DateTime)
    
    def __init__(self, job_dept, deptName, Salary, Description,date_r):
        self.job_dept = job_dept
        self.deptName = deptName
        self.Salary = Salary
        self.Description = Description
        self.date_registered = date_r
    # method to add department to database
    def add_department(dept_dict):
        new_dept = Department(
            job_dept = dept_dict['job_dept'],
            deptName = dept_dict['deptName'],
            Salary = dept_dict['Salary'],
            Description = dept_dict['Description'],
            date_r = dept_dict['date_registered'])
        # add to database and commit
        db.session.add(new_dept)
        db.session.commit()


# Model Position
class Position(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    deptID = db.Column(db.Integer, db.ForeignKey('department.id'), nullable = False)
    positionName = db.Column(db.String(100))
    date_registered = db.Column(db.DateTime)

    def __init__(self, deptID, pos, date_r):
        self.deptID = deptID
        self.positionName = pos
        self.date_registered = date_r

    # adding to Postion table

    def add_position(pos_dict):
        new_pos = Position(
            deptID = pos_dict['deptId'],
            pos = pos_dict['posName'],
            date_r = pos_dict['date_registered']
        )
        # add to database and commit
        db.session.add(new_pos)
        db.session.commit()
