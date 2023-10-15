# import SQLALchemy
import email
from App import db
from flask import request, redirect

# Define class Employee
class Payroll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    collageID = db.Column(db.Integer, db.ForeignKey('collage.id'), nullable=False)
    branchID = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=True)   
    deptID= db.Column(db.Integer, db.ForeignKey('department.id'), nullable = False)
    positionID = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False) 
    leaveID = db.Column(db.Integer, db.ForeignKey('leave.id'), nullable=True)   
    empID= db.Column(db.Integer, db.ForeignKey('employee.id'), nullable = False)
    salID = db.Column(db.Integer, db.ForeignKey('salary.id'), nullable=True) 
    report = db.Column(db.String(100))    
    date_registered = db.Column(db.DateTime)
    
    def __init__(self, collageID,branchID, deptID, positionID, leaveID,empID,salID, report, date_r):
        self.collageID = collageID
        self.branchID = branchID
        self.deptID = deptID
        self.positionID = positionID
        self.leaveID = leaveID
        self.empID = empID
        self.salID = salID
        self.report = report
        self.date_registered = date_r
    # method to add employee to database
    def add_payroll(emp_dict):
        new_payroll = Payroll(
        collageID = emp_dict['collageID'],
        branchID = emp_dict['branchID'],
        deptID = emp_dict['deptID'],
        positionID = emp_dict['positionID'],
        leaveID = emp_dict['leaveID'],
        empID = emp_dict['empID'],
        salID = emp_dict['salID'],
        report = emp_dict['report'],
        date_r = emp_dict['date_registered'])
        # add to database and commit
        db.session.add(new_payroll)
        db.session.commit()

#db.create_all()
