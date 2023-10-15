# Route to insert ComplainIssue
from models.modules import *
# Blueprint Configuration
employee_bp = Blueprint(
    'employee_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

# Initialize the SQLAlchemy data store and Flask-Security.
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

# Update the Position drop down values based on the selected Department
@employee_bp.route('/_update_department_position')
def update_department_position():
    # the value of the first dropdown (selected by the user)
    selected_department = request.args.get('selected_department_', type=str)
    # get values for the second dropdown
    updated_position_values = Dropdown.get_position_values()[selected_department]

    # create the value sin the dropdown as a html string
    html_position_selected = ''
    html_position_selected += '<option value="{}" disabled selected required>{}</option>'.format("Null", "--- Select ---")
    for entry in updated_position_values:
        html_position_selected += '<option value="{}">{}</option>'.format(entry, entry)

    return jsonify(html_position_selected=html_position_selected)

# method to get values of selected items
def get_values():
    department_position_relations = Dropdown.get_position_values()

    default_department = sorted(department_position_relations.keys())
    default_position_values = department_position_relations[default_department[0]]

    # store all values in the list
    list_values = [default_department, default_position_values]

    return list_values

# route to EmployeeDetail
@employee_bp.route('/employeeDetail/',methods=['POST', 'GET'])
@login_required
def employeeDetail():
    # Get the selected number of rows per page from the dropdown menu
    per_page = int(request.args.get('state', 5))  # Default to 10 rows per page if not selected

    # Get the current page number from the query parameters
    page = request.args.get('page', 1, type=int)
    try:
        selected_values = get_values()
        # Query all data from database
        if current_user.has_role('super-admin'):
            all_emp = db.session.query(Employee,Department,Position, Collage).select_from(Employee).join(
                Department, Department.id == Employee.deptID
            ).join(Position, Position.id == Employee.positionID).\
                join(Collage, Collage.id == Employee.collageID).all()


        else:
            all_emp = db.session.query(Employee,Department,Position, Branch).select_from(Employee).join(
                Department, Department.id == Employee.deptID
            ).join(Position, Position.id == Employee.positionID).\
                join(Branch, Branch.id == Employee.branchID).\
                filter(Employee.collageID==session['collage_id_branch']).\
                paginate(page=page, per_page=per_page, error_out=False)
                # (Employee.wereda_id == session['wereda_id'])).\
            

        depts = Department.query.order_by(Department.id.desc())
        pos = Position.query.order_by(Position.id.desc())
        return render_template('employeeDetail.html', employees = all_emp, departments = selected_values[0], roles = selected_values[1],  rows_per_page = per_page)

    except IndexError:
        flash("First Select Department")
        return redirect(url_for('dashboard'))

# route to newEmployee.html page
@employee_bp.route('/newEmployee/',methods=['POST', 'GET'])
@login_required
def newEmployee():
    selected_values = get_values()
    # Query all data from database
    all_emp = db.session.query(Employee,Department,Position).select_from(Employee).join(
        Department, Department.id == Employee.deptID
    ).join(Position, Position.id == Employee.positionID).all()

    depts = Department.query.order_by(Department.id.desc())
    pos = Position.query.order_by(Position.id.desc())
    return render_template('newEmployee.html', employees = all_emp, departments = selected_values[0], roles = selected_values[1])

# Render the pictures
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/uploads', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@employee_bp.route("/register_employee/",methods=['POST', 'GET'])
@login_required
def register_employee():
    if request.method == 'POST':
        # Add employee data to database
        # get deptID from Department under department name
        dept = Department.query.filter_by(deptName = request.form['deptID'])
        for row in dept:
            deptID = row.id
        # get positionID from Position under department name
        role = Position.query.filter_by(positionName = request.form['positionID'])
        for row in role:
            positionID = row.id
        
        deptID = deptID
        positionID = positionID
        branch_id = request.form.get('branchID')
        fname = request.form['fname']
        lname = request.form['lname']
        gender = request.form['gender']
        age = request.form['age']
        emp_email = request.form['emp_email']
        contact_add = request.form['contact_add']
        emp_pass = request.form['emp_pass']
        pic = save_picture(request.files['photo'])
        date_r = date.today()

        # add employee to database
        Employee.add_employee(
        {'deptID':deptID,
        'positionID':positionID, 'collageID':session['collage_id_branch'], 'branchID': branch_id,
        'fname':fname, 'lname':lname,
        'gender':gender, 'age':age,'emp_email':emp_email, 'emp_pass':emp_pass,
        'contact_add':contact_add,'photo':pic, 'date_registered':date_r})

        flash("Registration Successfully", 'success')

        return redirect(url_for('employee_bp.newEmployee'))
    else:

        return render_template('register_employee.html')

# Edit Employee Profile and redirect to editEmployee page
@employee_bp.route("/editEmployee/<int:id>",methods=['POST', 'GET'])
@login_required
def editEmployee(id):
    if request.method == 'GET':
        selected_values = get_values()
        edit_emp = db.session.query(Employee, Department, Position).\
        join(Department, Employee.deptID == Department.id).\
        join(Position, Employee.positionID == Position.id).filter(Employee.id == id).all()

        return render_template('editEmployee.html', emp = edit_emp, departments = selected_values[0], positions = selected_values[1])

# Update the employee profile based on employee id
@employee_bp.route('/updateEmployee/', methods=['POST', 'GET'])
@login_required
def updateEmployee():
    # get form values
    emp_id = request.form.get('empID')

    # get employee data based of id
    empl_data = Employee.query.filter_by(id = emp_id).first()
    # update the data    
    empl_data = request.form.get('branchID')
    empl_data = request.form['fname']
    empl_data = request.form['lname']
    empl_data = request.form['gender']
    empl_data = request.form['age']
    empl_data = request.form['emp_email']
    empl_data = request.form['contact_add']
    # empl_data = request.form['emp_pass']
    # update picture if picture uploaded
    if request.files['photo']:
        empl_data.photo = save_picture(request.files['photo'])

    # update department and position
    if request.form.get('dept'):
        # get deptID from Department under department name
        dept = Department.query.filter_by(deptName = request.form['deptID'])
        for row in dept:
          empl_data.department = row.id
        # get positionID from Position under department name
        pos = Position.query.filter_by(positionName = request.form['positionID'])
        for row in pos:
          empl_data.positionID = row.id

    db.session.commit()
    flash('Updated Successfully', 'success')
    return redirect(url_for('employee_bp.employeeDetail'))

# delete row from employee table
@employee_bp.route('/deleteEmployee/<int:id>', methods=['POST', 'GET'])
@login_required
def deleteEmployee(id):
    if request.method=='GET':
        deleted_emp = Employee.query.get(id)
        # excetion can't delete if appointment data available under this employee
        try:

            db.session.delete(deleted_emp)
            db.session.commit()
            flash('1 Data Deleted', 'danger')
            return redirect(url_for('employee_bp.employeeDetail'))
        except exc.IntegrityError:
            flash('Sorry, There is no Registered Data።', 'danger')
            return redirect(url_for('employee_bp.employeeDetail'))
