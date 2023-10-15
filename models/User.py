"""Database models."""
from App import db
from flask_login import current_user
from flask import redirect, url_for, abort, request
from flask_security import UserMixin, RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Create a table to support a many-to-many relationship between Users and Roles
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True )
    first_name = db.Column(db.String(100), nullable=True, unique=False )
    last_name = db.Column(db.String(100), nullable=True, unique=False )
    phone_number = db.Column(db.String(100), nullable=True, unique=False )
    email = db.Column(db.String(40), unique=True, nullable=False )
    password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False )
    collageID = db.Column(db.Integer, db.ForeignKey('collage.id'), nullable=True)
    branchID = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=True)
    confirmed_at = db.Column(db.DateTime, index=False, unique=False, nullable=True )
    active = db.Column(db.Boolean(), unique=False, nullable=False)
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )


    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)


    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('admin'):
            return True
        if current_user.has_role('super-admin'):
            return True
        if current_user.has_role('staff'):
            return True
        if current_user.is_anonymous(self):
            return False
        return False

    def _handle_view(self, name, **kwargs):
        """Override built in _handle_view in order to redirect users when a view is not accessible"""
        if not self.is_accessible():
            if current_user.is_authenticated:
                #permission denied
                abort(403)

            else:
                return redirect(url_for('dashboard_bp.dashboard'))

# Role class
class Role(db.Model, RoleMixin):

    # Our Role has three fields, ID, name and description
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    # __str__ is required by Flask-Admin, so we can have human-readable values for the Role when editing a User.
    # If we were using Python 2.7, this would be __unicode__ instead.
    def __str__(self):
        return self.name

    # __hash__ is required to avoid the exception TypeError: unhashable type: 'Role' when saving a User
    def __hash__(self):
        return hash(self.name)
