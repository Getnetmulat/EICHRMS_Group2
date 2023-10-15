# Route to insert ComplainIssue
from models.modules import *
# Blueprint Configuration
payroll_bp = Blueprint(
    'payroll_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

# Initialize the SQLAlchemy data store and Flask-Security.
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

# Update the Position drop down values based on the selected Department
@payroll_bp.route('/_update_department_position')
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

# route to Payroll
@payroll_bp.route('/payrollDetail/',methods=['POST', 'GET'])
@login_required
def payrollDetail():
    try:
        selected_values = get_values()
        # Query all data from database
        if current_user.has_role('super-admin'):
            all_emp = db.session.query(Payroll,Department,Position,Salary,Employee,Collage,Branch).select_from(Payroll).join(
                Department, Department.id == Payroll.deptID
            .join(Position, Position.id == Payroll.positionID).join(Salary,Salary.id ==Payroll.salID).
            json(Employee, Employee.id == Payroll.empID).join(Collage, Collage.id == Payroll.collageID).
            join(Branch,Branch.id == Payroll.branchID).all())


        else:
            all_emp = db.session.query(Payroll,Department,Position,Salary,Employee,Collage,Branch).select_from(Payroll).join(
                Department, Department.id == Payroll.deptID
            .join(Position, Position.id == Payroll.positionID).join(Salary,Salary.id ==Payroll.salID).
            json(Employee, Employee.id == Payroll.empID).join(Collage, Collage.id == Payroll.collageID).
            join(Branch,Branch.id == Payroll.branchID).filter((Payroll.collageID==session['collage_id_branch']) & (Payroll.branchID == session['branch_id'])).all())

        depts = Department.query.order_by(Department.id.desc())
        pos = Position.query.order_by(Position.id.desc())
        return render_template('payrollDetail.html', payrolls = all_emp, departments = selected_values[0], roles = selected_values[1])

    except IndexError:
        return redirect(url_for('dashboard'))
