
# import SQLALchemy
from App import db
from flask import request, redirect

# Model Salary
class Salary(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    collageID = db.Column(db.Integer, db.ForeignKey('collage.id'), nullable = False)
    deptID = db.Column(db.Integer, db.ForeignKey('department.id'), nullable = False)
    amount = db.Column(db.String(100))
    annual = db.Column(db.String(100))
    bonus = db.Column(db.String(100))
    date_registered = db.Column(db.DateTime)

    def __init__(self,collageID, deptID,amount,annual, bonus, date_r):
        self.collageID = collageID
        self.deptID = deptID
        self.amount = amount
        self.annual = annual
        self.bonus = bonus
        self.date_registered = date_r

    # adding to Salary table

    def add_salary(salary_dict):
        new_sal = Salary(
            collageID = salary_dict['collageID'],
            deptID = salary_dict['deptId'],
            amount = salary_dict['amount'],
            annual = salary_dict['annual'],
            bonus = salary_dict['bonus'],
            date_r = salary_dict['date_registered']
        )
        # add to database and commit
        db.session.add(new_sal)
        db.session.commit()
