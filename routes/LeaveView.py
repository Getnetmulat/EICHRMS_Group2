# import required modules from models
from models.modules import *
# Blueprint Configuration
leave_bp = Blueprint(
    'leave_bp', __name__,
    template_folder='templates',
    static_folder='static'
)
# Define Leave Class
class LeaveView:

    # Route to salary
    @leave_bp.route('/leave/', methods=['POST', 'GET'])
    @login_required
    def leave():
        # get all data from department and salary tables using one-to-many relationships
        all_leave = db.session.query(Salary, Employee).select_from(Salary).join(Employee).all()
        empName = Employee.query.order_by(Employee.id.asc())

        if request.method == 'POST':
            return render_template('salary.html', leaves = all_leave, empNames = empName)
        return render_template('salary.html', leaves = all_leave, empNames = empName)

    
