
# import SQLALchemy
from App import db
from flask import request, redirect

# Model leave
class Leave(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    empID = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable = False)
    reason = db.Column(db.String(100))
    leave_date = db.Column(db.DateTime)

    def __init__(self,empID, reason, leave_date):
        self.empID = empID
        self.reason = reason
        self.leave_date = leave_date

    # adding to Leave table

    def add_leave(leave_dict):
        new_leave = Leave(
            empID = leave_dict['empID'],
            reason = leave_dict['reason'],
            leave_date = leave_dict['leave_date']
        )
        # add to database and commit
        db.session.add(new_leave)
        db.session.commit()
