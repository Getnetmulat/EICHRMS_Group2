# import SQLALchemy
from App import db
from flask import request, redirect

# Define class Qualification
class Qualification(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    empID = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable = False)
    positionID = db.Column(db.Integer, db.ForeignKey('position.id'), nullable = False)
    requirements = db.Column(db.String(100))
    date_registered = db.Column(db.DateTime)
    
    def __init__(self, empID, positionID, requirements, date_r):
        self.empID = empID
        self.positionID = positionID
        self.requirements =requirements
        self.date_registered = date_r
    # method to add Qualification to database
    def add_qualification(quali_dict):
        new_qual = Qualification(
            empID = quali_dict['empID'],
            positionID = quali_dict['positionID'],
            requirements = quali_dict['requirements'],
            date_r = quali_dict['date_registered'])
        # add to database and commit
        db.session.add(new_qual)
        db.session.commit()
