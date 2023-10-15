
# auth.py
from App import db, app, login_manager
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from flask_security import *
from models.Collage import *
from models.User import *
from datetime import datetime

# Initialize the SQLAlchemy data store and Flask-Security.
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
# Executes before the first request is processed.
@app.before_first_request
def before_first_request():
    # Create the Roles "admin" and "end-user" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', description='collage Administrator')
    user_datastore.find_or_create_role(name='super-admin', description='Super Administrator')
    user_datastore.find_or_create_role(name='staff', description='Collage Staff')

    # Create  a default user for testing purposes -- unless they already exists.
    # In each case, use Flask-Security utility function to encrypt the password.
    encrypted_password = generate_password_hash('Admin@123')
    if not user_datastore.get_user('superadmin@eic.com'):
        # Create default collage for super admin
        Collage.add_collage({'collageName':'Emerald International Education', 'date_registered':datetime.today()})
        user_datastore.create_user(email='superadmin@eic.com', collageID=1, password=encrypted_password)

    # Commit any database changes; the User and Roles must exist before we can add a Role to the User
    db.session.commit()

    # Give one User has the "super-admin" role, while the other has the "admin" role. (This will have no effect if the
    # Users already have these Roles.) Again, commit any database changes.
    user_datastore.add_role_to_user('superadmin@eic.com', 'super-admin')
    # add default collage
    db.session.commit()

## Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@auth_bp.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method=='GET': # if the request is a GET we return the login page
        return render_template('login.html')
    else:
        """if the request is POST then we check if the user exist
        and with the rigth password
        """
        uname = request.form.get('username')
        password = request.form.get('password')
        #remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=uname).first()

        """"Check if the user actually exists
        take the user-suplied password, hash it , and compare it to the hashed password in the database.
        """
        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user:
            flash("Sorry! Username is not Correct!")
            return redirect(url_for('auth_bp.login', next=request.url))
        elif not check_password_hash(user.password, password):
            flash("Sorry! Password is not Correct!")
            return redirect(url_for('auth_bp.login', next=request.url))

        """ if the user doesn't exist or password is wrong, reload the page
          if the above check passes, then we know the user has the right credentials
        """
        # store the collageID of the user to session file for later use
        session['collage_id_branch'] = user.collageID
        session['branch_id'] = user.branchID


        login_user(user)

        return redirect(url_for('dashboard_bp.dashboard', next=request.url))


@auth_bp.route('/signup', methods=['POST'])
def signup():

    email = request.form.get('username')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    phone_number = request.form.get('phone_number')
    password = request.form.get('password')
    collageID = request.form.get('collageName_')
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email already exist')
        return redirect(url_for('auth_bp.login', next=request.url))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(first_name=fname, last_name=lname, phone_number=phone_number, email=email, password=generate_password_hash(password, method='sha256'), collageID=collageID, active=0)
    db.session.add(new_user)
    db.session.commit()
    # retrieve user_id and role_id
    user_datastore.add_role_to_user(email, 'admin')
    db.session.commit()
    flash('Successfully Registered', 'success')

    return redirect(url_for('auth_bp.login', next=request.url))

"""load all users on user_loader"""
# Load all users
@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


"""Logout- redirect to login page"""
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))

"""Handle unauthorized_handdler"""
@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash("Insert Password")
    return redirect(url_for('auth_bp.login'))

"""Change an existing user's password."""
@auth_bp.route('/change_password', methods=['POST', 'GET'])
@login_required
def change_password():
    try:
        if request.method=='POST':
            user = User.query.filter_by(id=current_user.id).first()
            if not check_password_hash(user.password, request.form.get('oldpassword')):
                flash("Sorry! Old Password is not Correct!")
                return redirect(url_for('dashboard_bp.dashboard'))
            else:
                user.password = generate_password_hash(request.form['newpassword'], method='sha256')
                db.session.commit()
                flash('The Password Changed', 'success')
                return redirect(url_for('auth_bp.login'))


    except Exception as e:
        print(e)
