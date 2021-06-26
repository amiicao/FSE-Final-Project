from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask import send_from_directory
import xlrd
from database import get_db
UPLOAD_FOLDER = 'uploads'
bp = Blueprint('class_teacher', __name__,url_prefix='/class_teacher')
from models import Classroom, TermCourse, Teacher, Application

@bp.route('/teachermain', methods=['POST', 'GET'])
def teachermain():
    return render_template('teachermain.html')


@bp.route('/submitapplication', methods=['POST', 'GET'])
def applicationsubmit():
    if request.method == 'POST':
        error = None
        teacher_id = request.form['teacher_id']
        content = request.form['content']
        # 0:未处理 1：处理完成 2：被拒绝
        statecode = 0
        if len(content) > 200:
            error = "字数超过上限！"
        elif content is None:
            error = "未填写内容！"
        else:
            applcation = Application(teacher_id=teacher_id, content=content, statecode=statecode)
            db = get_db()
            db.session.add(applcation)
            db.session.commit()
            error = "提交申请成功"
        flash(error)
    return redirect(url_for('classarrange.teachermain'))
