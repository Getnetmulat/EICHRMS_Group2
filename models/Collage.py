# import SQLALchemy
from App import db
from flask import request, redirect

# Define branch Lists
class Collage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    collageName = db.Column(db.String(200))
    date_registered = db.Column(db.DateTime)
    # initialize the relationship from the branch handler table with branch category table
    collage =  db.relationship('Branch', backref='branch', lazy = True)
    collage = db.relationship('User', backref='user_collage', lazy=True)

    def __init__(self, collageName, date_r):
        self.collageName = collageName
        self.date_registered = date_r

    # method to add collage to database
    def add_collage(collage_dict):
        new_collage = Collage(
            collageName = collage_dict['collageName'],
            date_r = collage_dict['date_registered'])
        # add to database and commit
        db.session.add(new_collage)
        db.session.commit()

# Model branch and Woreda or Address
class Branch(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    collageID = db.Column(db.Integer, db.ForeignKey('collage.id'), nullable = False)
    branchName = db.Column(db.String(100))
    date_registered = db.Column(db.Date)
    branch = db.relationship('User', backref='user_branch', lazy=True)
    # define constructor class Wereda
    def __init__(self, collageID, branchName, date_r):
        self.collageID = collageID
        self.branchName = branchName
        self.date_registered = date_r

    #adding to branch table
    def add_branch(branch_dict):
        new_branch = Branch(
            collageID = branch_dict['collageID'],
            branchName = branch_dict['branchName'],
            date_r = branch_dict['date_r']
        )
        # add to database and commit
        db.session.add(new_branch)
        db.session.commit()
