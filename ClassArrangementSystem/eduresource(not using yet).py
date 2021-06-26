from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask import send_from_directory
import xlrd
from database import get_db
UPLOAD_FOLDER = 'uploads'
bp = Blueprint('eduresource', __name__,url_prefix='/eduresource')
from models import Classroom, TermCourse, Teacher, Application


@bp.route('/add', methods=['POST', 'GET'])
# @login_required
def add():
    # form1 = Form1()
    # form2 = Form2()
    if request.method == 'POST':
        print(request.values)
        # if form1.submit1.data and form1.validate():
        location = request.form['location']
        print(location)
        capacity = request.form['capacity']
        campus = request.form['campus']
        db = get_db()
        error = None
        if not location:
            error = '缺少教室名称！'
        elif not capacity:
            error = '缺少教室容量'
        elif int(capacity) <= 0:
            error = "修改容量不能小于等于0！"
        elif int(capacity) > 500:
            error = "教室容量不能超过500人！"
        elif not campus:
            error = '缺少校区'
        if error is None:
            room = Classroom.query.filter_by(location=location, status=0).first()
            if room is not None:
                error = "已经存在该教室！"
            else:
                n = Classroom.query.filter_by(status=0).count()
                id = str(n + 1).zfill(3)
                classroom = Classroom(location=location, capacity=capacity, campus=campus, id=id, status=0)
                try:
                    db.session.add(classroom)
                    db.session.commit()
                    error = '添加教室:「' + location + "」成功!"
                except:
                    error = "添加教室失败！"
            print(error)
            # return redirect(url_for('classarrange.classroomarrange'))
            # return render_template('classroomarrange.html', error=error, Classroom=Classroom)
        flash(error)
    # Classrooms = Classroom.query.all()
    return redirect(url_for(''))


@bp.route('/allclassroom', methods=['POST', 'GET'])
def allclassroom():
    return render_template('classroomarrange.html')

@bp.route('/classroomarrange', methods=['POST', 'GET'])
def classroomarrange():
    Classrooms = Classroom.query.filter_by(status=0).all()
    return render_template('classroomarrange.html', Classrooms=Classrooms)

@bp.route('/classroommodify', methods=['POST', 'GET'])
def classroommodify():
    if request.method == 'POST':
        error = None
        capacity = request.form['capacity']
        location = request.form['location']
        campus = request.form['campus']
        classroom = Classroom.query.filter_by(location=location, status=0).first()
        if capacity:
            if int(capacity) <= 0:
                error = "修改容量不能小于等于0！"
            elif int(capacity) > 500:
                error = "教室容量不能超过500人！"
            else:
                classroom.capacity = capacity
                db = get_db()
                try:
                    db.session.commit()
                    error = "修改教室 " + location + " 容量为：「" + capacity + "」"
                except:
                    db.session.rollback()
                    return '修改出错！'
        if error:
            flash(error)
    return redirect(url_for('classarrange.classroomarrange'))

@bp.route('/muladd', methods=['POST', 'GET'])
def muladd():
    if request.method == 'POST':
        print(request.files)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('classarrange.classroomarrange'))
        file = request.files['file']
        bool = file.filename.endswith(".xls")
        if not bool:
            flash("上传文件类型必须是 .xls 文件 ！")
            return redirect(url_for('classarrange.classroomarrange'))
        print(file.filename)
        classrooms = xlrd.open_workbook(file_contents=file.read())
        db = get_db()
        try:
            table = classrooms.sheets()[0]
        except:
            flash("no sheet in %s named sheet1") % file.filename
            return redirect(url_for('classarrange.classroomarrange'))
        nrows = table.nrows
        ncols = table.ncols
        names = classrooms.sheet_names()
        status = classrooms.sheet_loaded(names[0])
        print(status)
        # print(os.getcwd(), "nrows %d, ncols %d") % (nrows, ncols)
        print(nrows)
        print(ncols)
        row_list = []
        error = "成功批量添加："
        flag = True
        for i in range(1, nrows):
            if not flag:
                break
            row_date = table.row_values(i)
            row_list.append(row_date)
            print(row_list)
            n = i - 1
            print(row_list[n])
            N = Classroom.query.filter_by(status=0).count()
            id = str(N + 1).zfill(3)
            if not row_list[n][0]:
                error = "缺少教室所在校区"
                flag = False
            elif not row_list[n][1]:
                error = "缺少教室名称"
                flag = False
            elif not row_list[n][2]:
                error = "缺少教室容量"
                flag = False
            else:
                try:
                    a = int(row_list[n][2])
                    if a <= 0:
                        error = "教室容量不得小于等于0！"
                        flag = False
                    elif a > 500:
                        error = "教室容量不得大于500！"
                        flag = False
                except:
                    error = "格式错误！"
                    flag = False

            classroom = Classroom(campus=row_list[n][0], location=row_list[n][1], capacity=row_list[n][2], id=id,
                                  status=0)
            try:
                db.session.add(classroom)
                error = error + "「" + str(row_list[n][1]) + "」"
                print(classroom)
                db.session.commit()
            except:
                error = "添加失败！"
                flag = False
                break
        flash(error)
    # # return redirect(url_for('library.addbook'))
    return redirect(url_for('classarrange.classroomarrange'))


def uploaded_file(filename):
    return send_from_directory(filename)

@bp.route('/query', methods=['POST', 'GET'])
# @login_required
def query():
    urls = "department"
    if request.method == 'POST':
        location = request.form['location']
        capacity = request.form['capacity']
        campus = request.form['campus']
        db = get_db()
        error = None
        if request.form['location'] is None and request.form['capacity'] is None and request.form['campus'] is None:
            flash("请输入查询条件 ！")
            return render_template(urls)
        if error is None:
            classrooms = Classroom.query.filter(
                Classroom.location.like("%" + location + "%") if location is not None else "",
                Classroom.capacity.like("%" + capacity + "%") if capacity is not None else "",
                Classroom.campus.like("%" + campus + "%") if campus is not None else "",
                Classroom.status == 0
            ).all()
            print(classrooms)
            if not classrooms:
                flash("教室不存在！")
                session['query'] = None
            else:
                session['query'] = 'yes'
                return render_template(urls + '.html', classrooms=classrooms)
        flash(error)
    return render_template(urls + '.html')
