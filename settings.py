import os
class Config(object):

    SECRET_KEY = os.urandom(32)
    basedir = os.path.abspath(os.path.dirname(__file__))
    # Enable debug mode.
    DEBUG = True
    # Connect to the database
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/eichrms_db'  #connect to MYSQL Database
    #SQLALCHEMY_DATABASE_URI = 'postgresql://eicds:eichrms/15@localhost:5432/eichrms_db' #connect to PostgreSQL Database
    
    
    # Turn off the Flask-SQLAlchemy event system and warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT =""
    USER_ENABLE_AUTH0 = False

    UPLOAD_FOLDER = '/static/uploads'
    ALLOWED_EXTENSIONS = {'zip','pdf', 'docx', 'doc', 'mp3','mp4','png', 'jpg', 'jpeg'}
