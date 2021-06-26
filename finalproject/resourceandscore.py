import datetime
import functools
# from flask_filer import FileField, FileRequired, FileAllowed
import os.path
import time

import xlrd
from flask_login import login_required, current_user
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
bp = Blueprint('resourceandscore', __name__, url_prefix='/resourceandscore')



# @bp.route('/')  # 首页(侧边栏)
# def student_analysis():
#     return render_template('sidebar_S.html')


@bp.route('/student_HW')   # 作业提交_学生
def student_HW():
    return render_template('ResourceandScore/student_HW.html')


@bp.route('/student_marks')   # 成绩查询_学生
def score_analysis():
    return render_template('ResourceandScore/student_marks.html')


@bp.route('/student_analysis')   # 成绩分析_学生
def student_analysis():
    return render_template('ResourceandScore/student_analysis.html')


@bp.route('/teacher_resource')   # 资源分享_教师
def resource_management():
    return render_template('ResourceandScore/teacher_resource.html')


@bp.route('/teacher_HW')   # 作业布置_教师
def teacher_HW():
    return render_template('ResourceandScore/teacher_HW.html')


@bp.route('/teacher_marks')   # 成绩录入_教师
def teacher_marks():
    return render_template('ResourceandScore/teacher_marks.html')


@bp.route('/score_analysisT')   # 成绩分析_教师
def score_analysisT():
    return render_template('ResourceandScore/teacher_analysis.html')


@bp.route('/score_request')   # 成绩修改_教师/管理员
def score_request():
    return render_template('ResourceandScore/score_request.html')