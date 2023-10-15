# import required modules from models
from models.modules import *
# Blueprint Configuration
salary_bp = Blueprint(
    'salary_bp', __name__,
    template_folder='templates',
    static_folder='static'
)
# Define Salary Class
class salaryView:

    # Route to salary
    @salary_bp.route('/salary/', methods=['POST', 'GET'])
    @login_required
    def salary():
        # get all data from department and salary tables using one-to-many relationships
        all_pos = db.session.query(Salary, Department).select_from(Salary).join(Department).all()
        deptName = Department.query.order_by(Department.id.asc())

        if request.method == 'POST':
            return render_template('salary.html', salarys = all_pos, depNames = deptName)
        return render_template('salary.html', salarys = all_pos, depNames = deptName)

