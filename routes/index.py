from models.modules import *
import numpy as np
import matplotlib.pyplot as plt
## Blueprint Configuration
dashboard_bp = Blueprint(
    'dashboard_bp', __name__,
    template_folder='templates',
    static_folder='static'
)
@dashboard_bp.route('/', methods=['GET'])
# route page to index/login
def index():
    regionNames = Collage.query.all()
    try:
        return render_template('login.html', regionNames = regionNames)
    except TemplateNotFound:
        abort(404)
#
@dashboard_bp.route('/dashboard/', methods=['GET'])
@login_required
# route page to index/login
def dashboard():

    count = Collage.query.count()

    collage_id = db.session.query(User.collageID).filter(User.id==current_user.id).first() # get Collage ID of the current user
    branch_count = db.session.query(Branch).filter(Branch.collageID==collage_id[0]).count() # count the number of rows of Campus
    emp_count = db.session.query(Employee).filter(Employee.collageID==collage_id[0]).count() # count the number of rows of Employee
    dep_count = db.session.query(Department).count() # count the number of rows of Department
    pos_count = db.session.query(Position).count() # count the number of rows of Position
    
    return render_template('dashboard.html', collage_count = count, branch_count = branch_count,  emp_count = emp_count, dep_count = dep_count, pos_count = pos_count)
