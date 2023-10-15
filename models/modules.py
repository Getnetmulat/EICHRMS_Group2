from flask_login.utils import login_required
from App import app
from flask import Blueprint, redirect,url_for, Response,render_template,request, abort, flash, jsonify, session
from flask_security import *

# import models class
from models.Collage import *
from models.User import *
from models.Dropdown import Dropdown
from models.FileUpload import UploadFile
from datetime import datetime, date
from models.Department import *
from models.Employee import *
from models.Salary import *
from models.Qualification import *
from models.Leave import *
from models.Payroll import *
