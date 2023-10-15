
# import SQLALchemy
import email
from App import db
from flask import request, redirect

# Define class Employee
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    collageID = db.Column(db.Integer, db.ForeignKey('collage.id'), nullable=False)
    branchID = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=True)   
    deptID= db.Column(db.Integer, db.ForeignKey('department.id'), nullable = False)
    positionID = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False) 
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    age = db.Column(db.String(100))
    contact_add = db.Column(db.String(100))
    emp_email = db.Column(db.String(100))
    emp_pass = db.Column(db.String(100))
    photo = db.Column(db.String(100))
    date_registered = db.Column(db.DateTime)
    # initialize the relationship from the department handler table with department category table
    # employee =  db.relationship('CollageID', backref='collage_employee', lazy = True)
    # employee =  db.relationship('branchID', backref='branch_employee', lazy = True)
    
    def __init__(self, collageID, branchID, deptID, positionID, fname, lname, gender, age, contact_add, emp_email, emp_pass, photo, date_r):
        self.collageID = collageID
        self.branchID = branchID
        self.deptID = deptID
        self.positionID = positionID
        self.fname = fname
        self.lname = lname
        self.gender = gender
        self.age = age
        self.contact_add = contact_add
        self.emp_email = emp_email
        self.emp_pass = emp_pass
        self.photo = photo
        self.date_registered = date_r
    # method to add employee to database
    def add_employee(emp_dict):
        new_emp = Employee(
        collageID = emp_dict['collageID'],
        branchID = emp_dict['branchID'],
        deptID = emp_dict['deptID'],
        positionID = emp_dict['positionID'],
        fname = emp_dict['fname'],
        lname = emp_dict['lname'],
        gender = emp_dict['gender'],
        age = emp_dict['age'],
        contact_add = emp_dict['contact_add'],
        emp_email = emp_dict['emp_email'],
        emp_pass = emp_dict['emp_pass'],
        photo = emp_dict['photo'],
        date_r = emp_dict['date_registered'])
        # add to database and commit
        db.session.add(new_emp)
        db.session.commit()

#db.create_all()
