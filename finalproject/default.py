import datetime
import functools
# from flask_filer import FileField, FileRequired, FileAllowed
import os.path
import time

import xlrd
from sqlalchemy import or_, and_, text
# from openpyxl import load_workbook
from flask import send_from_directory
from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask import send_from_directory
import xlrd
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from xlrd import open_workbook
from xlrd.timemachine import xrange

from werkzeug.exceptions import abort
# from uploads import ALLOWED_EXTENSIONS
# from user import login_required
from database import get_db

# import pandas as pd

UPLOAD_FOLDER = 'uploads'
bp = Blueprint('default', __name__)
# from models import Application,Classroom,Course,Teacher,TermCourse

# bp = Blueprint('classarrange', __name__, url_prefix='/classarrange')
from models import Classroom, TermCourse, Teacher, Application


@bp.route('/')
def hello_world():
    return render_template('sidebar.html')
