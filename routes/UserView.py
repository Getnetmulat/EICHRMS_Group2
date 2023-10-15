from models.modules import *

# Initialize the SQLAlchemy data store and Flask-Security.
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# Blueprint Configuration
user_mg_bp = Blueprint(
    'user_mg_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

"""  UserView class will do the following activities
    - register new user
    - Update specific user
    - Delete specific user
    - Activate / Deactivate specific user
    - Manage User's role
    - etc
"""
class UserView(object):
    # retrieving list of all users with relation to collage and roles
    @user_mg_bp.route('/userList/', methods=['POST', 'GET'])
    @login_required
    def userList():
        if request.method=='GET':
            try:

                collages = db.session.query(Collage).all() # query collages for dropdown menu
                roles = db.session.query(Role).all() # get all roles to dropdown menu
                # query all list of users with associations
                userlist = db.session.query(User, Collage, roles_users, Role).select_from(User).\
                join(Collage).join(roles_users).join(Role).\
                filter((roles_users.c.user_id == User.id) & (roles_users.c.role_id == Role.id) & (User.branchID==None)).all()
                return render_template('user/userList.html', users = userlist, collages=collages, roles=roles)
            except Exception as e:
                print('Error')

    """ route method to register new user by super-admin """
    @user_mg_bp.route('/registerUser', methods=['POST', 'GET'])
    @login_required
    def registerUser():
        if request.method=='POST':
            try:
                
                fname = request.form['fname']
                lname = request.form['lname']
                email = request.form['email']
                password = request.form['password']
                phone_number = request.form['phone_number']
                collageID = request.form['collageName_']
                role = request.form['roleName']

                if not request.form.get('userActive'):
                    active = 0
                else:
                    active = 1
                print(active)
                date_confirmed = datetime.today()
                
                user = User.query.filter_by(email=email).first()
                if user:
                    flash("The Email already Exist", 'danger')
                    return redirect(url_for('user_mg_bp.userList'))
                # create new user with the form data. Hash the password so plaintext version isn't saved.
                new_user = User(first_name=fname, last_name=lname, phone_number=phone_number,
                email=email, password=generate_password_hash(password, method='sha256'),
                collageID=collageID, active=active, confirmed_at=date_confirmed)
                db.session.add(new_user) # add user data to user table
                db.session.commit()
                # retrieve user_id and role_id
                user_datastore.add_role_to_user(email, role)
                db.session.commit()
                flash('REgistered Successfully', 'success')
                return redirect(url_for('user_mg_bp.userList'))

            except Exception as e:
                print(e)


    """ route method to register new user by admin """
    @user_mg_bp.route('/registerbranchUser', methods=['POST', 'GET'])
    @login_required
    def registerbranchUser():
        if request.method=='POST':
            try:
                """Try to register user if there are no errors that the exception catches"""
                # get all values from the form filled by user
                fname = request.form['fname'].strip()
                lname = request.form['lname'].strip()
                email = request.form['email'].strip()
                password = request.form['password'].strip()
                phone_number = request.form['phone_number'].strip()
                collageID = session['collage_id_branch']
                branch_id = request.form['branchName_']
                role ="admin"

                if not request.form.get('userActive'):
                    active = 0
                else:
                    active = 1
                print(active)
                date_confirmed = datetime.today()
                """ Check that the email is already exist in the databse. Return
                error message if the email is exist
                if this returns a user, then the email already exists in the database"""
                user = User.query.filter_by(email=email).first()
                if user:
                    flash("The Email already Exist", 'danger')
                    return redirect(url_for('user_mg_bp.userInfo', id=session['collage_id_branch']))
                # create new user with the form data. Hash the password so plaintext version isn't saved.
                new_user = User(first_name=fname, last_name=lname, phone_number=phone_number,
                email=email, password=generate_password_hash(password, method='sha256'),
                collageID=collageID, branchID = branch_id, active=active, confirmed_at=date_confirmed)
                db.session.add(new_user) # add user data to user table
                db.session.commit()
                # retrieve user_id and role_id
                user_datastore.add_role_to_user(email, role)
                db.session.commit()
                flash('Successfully Registered', 'success')
                return redirect(url_for('user_mg_bp.branchUser', id=session['collage_id_branch']))

            except Exception as e:
                print(e)

    """ Edit a user profile
    the method route to edit page when the data is found with the same user id """
    @user_mg_bp.route('/editUser/<int:id>', methods=['POST', 'GET'])
    @login_required
    def editUser(id):
        try:
            if request.method=='GET':
                """ retreive data from user table if row found """
                collages = db.session.query(Collage).all() # query collages for dropdown menu
                roles = db.session.query(Role).all() # get all roles to dropdown menu
                # query all list of users with associations
                userData = db.session.query(User, Collage, roles_users, Role).select_from(User).\
                join(Collage).join(roles_users).join(Role).\
                filter((roles_users.c.user_id == User.id) & (roles_users.c.role_id == Role.id) & (User.id==id)).all()
                # Save role name in session for later use
                for row, reg, _, _, role in userData:
                    session['role_name'] = role.name

                return render_template('user/editUser.html', userData=userData, collages=collages, roles=roles)
        except Exception as e:
            print(e)

    """ Edit a branch user profile
    the method route to edit page when the data is found with the same user id """
    @user_mg_bp.route('/editBranchUser/<int:id>', methods=['POST', 'GET'])
    @login_required
    def editBranchUser(id):
        try:
            if request.method=='GET':
                """ retreive data from user table if row found """
                branchs = db.session.query(Branch).filter(Branch.collageID == session['collage_id_branch']).all() # query collages for dropdown menu
                roles = db.session.query(Role).all() # get all roles to dropdown menu
                # query all list of users with associations
                userData = db.session.query(User, Branch, roles_users, Role).select_from(User).\
                join(Branch).join(roles_users).join(Role).\
                filter((roles_users.c.user_id == User.id) & (roles_users.c.role_id == Role.id) & (User.id==id)).all()
                # Save role name in session for later use
                for row, reg, _, _, role in userData:
                    session['role_name'] = role.name

                return render_template('user/editbranchUser.html', userData=userData, branchs=branchs, roles=roles)
        except Exception as e:
            print(e)

    """ User info / branch's users information
    the method route to userInfo when the data is found with the same user id """
    @user_mg_bp.route('/branchUser/<int:id>', methods=['POST', 'GET'])
    @login_required
    def branchUser(id):
        try:
            if request.method=='GET':
                """ retreive data from user table if row found """
                branchs = db.session.query(Branch).filter(Branch.collageID==id).all() # query collages for dropdown menu
                roles = db.session.query(Role).all() # get all roles to dropdown menu
                # store collageID to session for later use
                userData = db.session.query(User, Collage, Branch, roles_users, Role).select_from(User).\
                join(Collage).join(Branch).join(roles_users).join(Role).\
                filter((roles_users.c.user_id == User.id) & (roles_users.c.role_id == Role.id) &(User.branchID==Branch.id) & (User.collageID==id)).all()
                # Save role name in session for later use
                print(userData)

                return render_template('user/branchUser.html', userData=userData, branchs=branchs, roles=roles)
        except Exception as e:
            print(e)

    """Update specified user """
    @user_mg_bp.route("/updateUser", methods=['POST', 'GET'])
    @login_required
    def updateUser():
        try:
            if request.method=='POST':
                user_id = request.form['id']
                """ Retrieve the user data if the row is found """

                userUpdate = User.query.filter_by(email=request.form['email']).first()
                """Update the user data based of the value of the form """
                userUpdate.first_name = request.form['fname'].strip()
                userUpdate.last_name = request.form['lname'].strip()
                userUpdate.phone_number = request.form['phone_number'].strip()

                userUpdate.collageID = request.form['collageName_'].strip()
                # check and update if password field is not empty
                if request.form['password'].strip():
                    userUpdate.password = generate_password_hash(request.form['password'].strip(), method='sha256')
                # Update the user is_active or not through the mycheckbox
                if request.form.get('userActive'):
                    userUpdate.active = 1
                else:
                    userUpdate.active = 0
                # update date confirmed
                userUpdate.confirmed_at = datetime.today()
                # check that the old user role is updated
                if request.form.get('roleName'):
                    # remove the user role
                    user_datastore.remove_role_from_user(request.form['email'], session['role_name'])
                    # add the updated user role
                    find_role = user_datastore.add_role_to_user(request.form['email'], request.form['roleName'])

                db.session.commit()
                flash("Updated Successfully", 'success')
                return redirect(url_for('user_mg_bp.userList'))
        except Exception as e:
            print(e)

    """Update branch user """
    @user_mg_bp.route("/updateBranchUser", methods=['POST', 'GET'])
    @login_required
    def updateBranchUser():
        try:
            if request.method=='POST':
                user_id = request.form['id']
                """ Retrieve the user data if the row is found """

                userUpdate = User.query.filter_by(email=request.form['email']).first()
                """Update the user data based of the value of the form """
                userUpdate.first_name = request.form['fname'].strip()
                userUpdate.last_name = request.form['lname'].strip()
                userUpdate.phone_number = request.form['phone_number'].strip()
                userUpdate.branchID = request.form['branchName_'].strip()
                # check and update if password field is not empty
                if request.form['password'].strip():
                    userUpdate.password = generate_password_hash(request.form['password'].strip(), method='sha256')
                # Update the user is_active or not through the mycheckbox
                if request.form.get('userActive'):
                    userUpdate.active = 1
                else:
                    userUpdate.active = 0
                # update date confirmed
                userUpdate.confirmed_at = datetime.today()
                # check that the old user role is updated
                if request.form.get('roleName'):
                    # remove the user role
                    user_datastore.remove_role_from_user(request.form['email'], session['role_name'])
                    # add the updated user role
                    find_role = user_datastore.add_role_to_user(request.form['email'], request.form['roleName'])

                db.session.commit()
                flash("Updated Successfully", 'success')
                if current_user.has_role('admin'):

                    return redirect(url_for('user_mg_bp.branchUser', id=session['collage_id_branch']))
                return redirect(url_for('user_mg_bp.userList'))
        except Exception as e:
            print(e)

    """ Delete specified user """
    @user_mg_bp.route('/delete/<int:id>', methods=['POST', 'GET'])
    @login_required
    def delete(id):
        try:
            if request.method =='GET':
                # get specified user
                user = user_datastore.get_user(id)
                # delete specified user
                user_datastore.delete_user(user)
                db.session.commit()
                # flash message
                flash('{} Deleted'.format(user), 'danger')
                return redirect(url_for('user_mg_bp.userList'))
        except Exception as e:
            print(e)
        except TypeError as e:
            print(e)
