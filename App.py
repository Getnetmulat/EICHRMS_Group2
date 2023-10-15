
# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#patch_all()
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth_bp.login'
login_manager.login_message = "Credential Account is Mandatory to access this Page!"
login_manager.login_message_category = "info"
# Construct the core app object
app = Flask(__name__, instance_relative_config=False)

# Application configuration
app.config.from_object("settings.Config")

# Initialize Plugins
db.init_app(app)
login_manager.init_app(app)
with app.app_context():
    #from routes import routes
    from routes import index, auth, collage, PayrollView,EmployeeView
    from routes import UserView, PositionView, DepartmentView, SalaryView,QualificationView, LeaveView

    # Register Blueprints
    app.register_blueprint(index.dashboard_bp)
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(collage.collage_bp)
    app.register_blueprint(UserView.user_mg_bp)
    app.register_blueprint(PositionView.position_bp)
    app.register_blueprint(DepartmentView.department_bp)
    app.register_blueprint(EmployeeView.employee_bp)
    app.register_blueprint(SalaryView.salary_bp)
    app.register_blueprint(QualificationView.qualification_bp)
    app.register_blueprint(LeaveView.leave_bp)
    app.register_blueprint(PayrollView.payroll_bp)

    # Creates Database models
    db.create_all()
