# Route to insert ComplainIssue
from models.modules import *
# Blueprint Configuration
department_bp = Blueprint(
    'department_bp', __name__,
    template_folder='templates',
    static_folder='static'
)
class DepartmentView:

    # Route to department
    @department_bp.route("/viewDepartment/",methods=['POST', 'GET'])
    @login_required
    def viewDepartment():
        # Query all list of departments
        all_dept = Department.query.order_by(Department.id.asc())
        if request.method == 'POST':
            return render_template('department.html', departments = all_dept)
        return render_template('department.html', departments = all_dept)

    # Route to insert department
    @department_bp.route("/insert_department",methods=['POST', 'GET'])
    @login_required
    def insert_department():
        if request.method == 'POST':
            
            # for dept in depts:

                # add employee to database
            Department.add_department(
                {'deptName': request.form['deptName'],
                'job_dept' : request.form['job_dept'],
                'Salary' : request.form['Salary'],
                'Description': request.form['Description'],
                'date_registered':date.today()})
                # Department.add_department(
                #     {'deptName':dept,
                #     'date_registered':date.today()})

            flash("Successfully Registerd", 'success')

            return redirect(url_for('department_bp.viewDepartment'))
        return render_template('viewDepartment.html')
    # deleting a single record from the Region table
    @department_bp.route('/deleteDepartment/<int:id>/', methods=['GET', 'POST'])
    @login_required
    def deleteDepartment(id):
        try:

            if request.method == 'GET':
                reg_del = Department.query.get(id)
                db.session.delete(reg_del)
                db.session.commit()
                flash('1 Data Deleted'.format(), 'danger')
                return redirect(url_for('department_bp.viewDepartment'))
        except exc.IntegrityError:
            flash("Can't be Deleted", 'danger')
            return redirect(url_for('department_bp.viewDepartment'))

    # row value in the database through ajax
    @department_bp.route('/update', methods=['GET', 'POST'])
    @login_required
    def update():
        try:
            if request.method == 'POST':
                field = request.form['field']
                value = request.form['value']
                editid = request.form['id']
                # store columnName in session
                session['fieldName'] = None
                # Update the deptName if the field or column name is deptName
                if field == 'deptName':
                    updatedName = Department.query.filter_by(id=editid).first()
                    updatedName.deptName = value.strip()
                    session['fieldName'] = 'deptName'
                # Update the collageName if the field or column name is collageName
                if field == 'collageName':
                    updatedName = Collage.query.filter_by(id=editid).first()
                    updatedName.collageName = value.strip()
                    session['fieldName'] = 'collageName'

                # Update the collageName if the field or column name is collageName
                if field == 'collageName':
                    updatedName = Collage.query.filter_by(id=editid).first()
                    updatedName.collageName = value.strip()
                    session['fieldName'] = 'collageName'

                if field == 'deptID':
                    updatedName = Position.query.filter_by(id=editid).first()
                    updatedName.deptID = value.strip()
                    session['fieldName'] = 'deptID'
                # update the collageName if the field or column name is collageName
                if field == 'positionName':
                    session['fieldName'] = 'positionName'
                    updatedName = Position.query.filter_by(id=editid).first()
                    updatedName.positionName = value.strip()
                db.session.commit() # commit to the databse
                success = 1 # update the success to 1, it  mean True if the column value is updated
                #return redirect('region_bp.region')
            return jsonify(success) # return success message
        except Exception as e:
            print(e)
