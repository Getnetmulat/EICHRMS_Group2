# import required modules from models
from models.modules import *
# Blueprint Configuration
position_bp = Blueprint(
    'position_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

class PositionView:

    # Route to Position
    @position_bp.route('/position/', methods=['POST', 'GET'])
    @login_required
    def position():
        # get all data from department and position tables using one-to-many relationships
        all_pos = db.session.query(Position, Department).select_from(Position).join(Department).all()
        deptName = Department.query.order_by(Department.id.asc())

        if request.method == 'POST':
            return render_template('position.html', positions = all_pos, depNames = deptName)
        return render_template('position.html', positions = all_pos, depNames = deptName)

    # route to insert_position
    @position_bp.route("/insert_position/", methods=['POST', 'GET'])
    @login_required
    def insert_position():

        if request.method == 'POST':

            pos_list = request.form.getlist('newFieldText[]')
            for value in pos_list:
                Position.add_position({
                'deptId':request.form['deptName'],
                'posName':value,
                'date_registered':date.today()
                })
            flash("Successfully Registered!")

            return redirect(url_for('position_bp.position'))
        return render_template('position_bp.position.html')

    # deleting a single record from the Position table
    @position_bp.route('/deletePosition/<int:id>/', methods=['GET', 'POST'])
    @login_required
    def deletePosition(id):
        try:

            if request.method == 'GET':
                reg_del = Position.query.get(id)
                db.session.delete(reg_del)
                db.session.commit()
                flash('1 Data Deleted'.format(), 'danger')
                return redirect(url_for('position_bp.position'))
        except exc.IntegrityError:
            flash("Can't be Deleted", 'danger')
            return redirect(url_for('position_bp.position'))
