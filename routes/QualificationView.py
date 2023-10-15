# Route to insert ComplainIssue
from models.modules import *
# Blueprint Configuration
qualification_bp = Blueprint(
    'qualification_bp', __name__,
    template_folder='templates',
    static_folder='static'
)
class qualificationView:

    # Route to qualification
    @qualification_bp.route("/viewqualification/",methods=['POST', 'GET'])
    @login_required
    def viewqualification():
        # Query all list of qualifications
        all_dept = Qualification.query.order_by(Qualification.id.asc())
        if request.method == 'POST':
            return render_template('qualification.html', qualifications = all_dept)
        return render_template('qualification.html', qualifications = all_dept)

