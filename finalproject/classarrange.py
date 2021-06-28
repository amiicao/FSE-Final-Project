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
import classarrange
from database import get_db

# import pandas as pd

UPLOAD_FOLDER = 'uploads'
bp = Blueprint('classarrange', __name__, url_prefix='/classarrange')
# from models import Application,Classroom,Course,Teacher,TermCourse

# bp = Blueprint('classarrange', __name__, url_prefix='/classarrange')
from models import Classroom, TermCourse, Course, User, Teacher, ModifyApplication


@bp.route('/')
def hello_world():
    return render_template('sidebar.html')


@bp.route('/hello')
def test():
    print("a")
    return "Hello"


@bp.route('/class_schedule')
@login_required
def class_schedule():
    a = []
    period = ["08:00~09:35", "09:50~11:25", "11:30~12:15", "13:15~14:50",
              "14:55~15:40", "15:55~17:30", "18:30~20:05", "20:10~20:55"]
    for i in range(8):
        tmp = [period[i]]
        for j in range(5):
            tmp.append(" ")
        a.append(tmp)
    b = [1, 2, 4, 6, 7]  # 221 212 21
    teacher = User.query.filter(User.status == "教师").first()
    courses = Course.query.filter().all()
    Classrooms = Classroom.query.filter(Classroom.status == 0).all()
    location = []
    for c in Classrooms:
        location.append(c)
    for c in courses:
        for i in [0, 7]:
            if c.time[i] == '0':
                break
            else:
                classroom = Classroom.query.filter(
                    Classroom.id == c.time[i + 4:i + 7] and Classroom.status == 0).first()
                # classroom = location[int(c.time[i + 4:i + 7])]
                print(classroom.location)
                if classroom.location == request.args.get('name'):
                    a[b[int(c.time[i + 2]) - 1] - 1][int(c.time[i + 1])] = c.name
                    if (c.time[i] == "3"):
                        a[b[int(c.time[i + 2]) - 1]][int(c.time[i + 1])] = c.name
    print(a)
    return render_template('ClassArrange/class_schedule.html', tables=a)


def decoder(s):  # 解码器
    a = [["周一", "周二", "周三", "周四", "周五"], \
         ["08:00", "09:50", "13:15", "15:55", "18:30"], \
         ["09:35", "11:25", "14:55", "17:30", "20:05"],
         ["09:35", "12:15", "15:40", "17:30", "20:55"]]
    haha = ["", ""]
    for i in [0, 7]:
        if s[i] == "0":
            if i == 7:
                haha += "\n"
            break
        else:
            haha[i // 7] += a[0][int(s[i + 1]) - 1] + ":"
            haha[i // 7] += a[1][int(s[i + 2]) - 1]
            haha[i // 7] += "-"
            haha[i // 7] += a[int(s[i])][int(s[i + 2]) - 1]

    return haha


@bp.route('/classmodify', methods=['POST', 'GET'])
@login_required
def classmodify():
    period = ["08:00~09:35", "09:50~11:25", "11:30~12:15", "13:15~14:50",
              "14:55~15:40", "15:55~17:30", "18:30~20:05", "20:10~20:55"]
    periods = {"0": "1", "1": "2", "2": "2", "3": "3", "4": "3", "5": "4", "6": "5", "7": "5"}
    daytime = {"周一": 1, "周二": 2, "周三": 3, "周四": 4, "周五": 5}
    if request.method == 'POST':
        # oldlocation = request.form['oldloaction']

        print(request)
        course_name = request.form['name']
        daytime1 = request.form['daytime1']
        periods1 = request.form['periods1']
        daytime2 = request.form['daytime2']
        periods2 = request.form['periods2']
        print('gggfsfsfsfsfs')
        location = request.form['classroom1']
        print('gggfsfsfs1fsfs')
        # flash(course_name)
        # flash(daytime1)
        # flash(daytime2)
        # flash(periods1)
        # pass
        print('fsfsfsfsfs')
        classroom = Classroom.query.filter_by(location=location).first()
        print(classroom.location)
        ID = classroom.id
        termCourse = Course.query.filter_by(name=course_name).first()
        # 生成timecode
        # 一共14位，假设每个课程最多有两时间阶段，也就是前七位和后七位，
        # 因此单独分析七位即可，0000000代表该时间段无课程，
        # 第一位代表课时，第二位代表周几（1-5），第三位代表每天的时间段（1-5，按照23323划分一天），
        # 第四位代表校区，后三位代表教室编号
        timecode = [termCourse.time[i] for i in range(len(termCourse.time))]
        if request.form['classroom1']:
            for i in range(3):
                timecode[i + 4] = ID[i]
                timecode[i + 11] = ID[i]
                print(i)
        print('hhh', request.form['daytime1'], request.form['daytime2'], request.form['periods1'])
        if request.form['daytime1']:
            timecode[1] = str(int(request.form['daytime1']) + 1)
        if request.form['daytime2']:
            timecode[1 + 7] = str(int(request.form['daytime2']) + 1)
        if request.form['periods1']:
            print(request.form['periods1'])
            timecode[2] = periods[request.form['periods1']]
        if request.form['periods2']:
            timecode[2 + 7] = periods[request.form['periods2']]
        timecode = ''.join(timecode)
        print(timecode)
        termCourse.time = timecode

        db = get_db()
        db.session.commit()

        error = '修改成功!'
        flash(error)
    return redirect(url_for('classarrange.department'))
    # return render_template('department.html')


# def classmodify():
#     period = ["08:00~09:35", "09:50~11:25", "11:30~12:15", "13:15~14:50",
#               "14:55~15:40", "15:55~17:30", "18:30~20:05", "20:10~20:55"]
#     if request.method == 'POST':
#         # oldlocation = request.form['oldloaction']
#
#         print(request)
#         course_name = request.form['name']
#         daytime1 = request.form['daytime1']
#         periods1 = request.form['periods1']
#         daytime2 = request.form['daytime2']
#         periods2 = request.form['periods2']
#         print('gggfsfsfsfsfs')
#         location = request.form['classroom1']
#         print('gggfsfsfs1fsfs')
#         # flash(course_name)
#         # flash(daytime1)
#         # flash(daytime2)
#         # flash(periods1)
#         # pass
#         print('fsfsfsfsfs')
#         classroom = Classroom.query.filter_by(location=location).first()
#         print(classroom.location)
#         ID = classroom.id
#         termCourse = TermCourse.query.filter_by(course_name=course_name).first()
#         # 生成timecode
#         # 一共14位，假设每个课程最多有两时间阶段，也就是前七位和后七位，
#         # 因此单独分析七位即可，0000000代表该时间段无课程，
#         # 第一位代表课时，第二位代表周几（1-5），第三位代表每天的时间段（1-5，按照23323划分一天），
#         # 第四位代表校区，后三位代表教室编号
#         timecode = [termCourse.time[i] for i in range(len(termCourse.time))]
#         if request.form['classroom1']:
#             pass
#             for i in range(3):
#                 timecode[i + 4] = ID[i]
#                 timecode[i + 11] = ID[i]
#                 print(i)
#             timecode = ''.join(timecode)
#             print(timecode)
#         if periods1:
#             pass
#             timecode
#         if periods2:
#             pass
#             timecode
#         termCourse.time = timecode
#
#         db = get_db()
#         db.session.commit()
#
#         error = '修改成功!'
#         flash(error)
#     return redirect(url_for('classarrange.department'))
#     # return render_template('department.html')
@login_required
def homepage():
    a = []
    period = ["08:00~09:35", "09:50~11:25", "11:30~12:15", "13:15~14:50",
              "14:55~15:40", "15:55~17:30", "18:30~20:05", "20:10~20:55"]
    for i in range(8):
        tmp = [period[i]]
        for j in range(5):
            tmp.append(" ")
        a.append(tmp)
    b = [1, 2, 4, 6, 7]  # 221 212 21
    teacher = User.query.filter(User.name == g['name']).first()
    print(teacher)
    if not teacher:
        teacher = User.query.filter(User.uid == current_user.uid).first()
        applications = ModifyApplication.query.filter_by(teacher_id=teacher.uid).all()

    name = teacher.teacher_name
    error = None
    if teacher:
        teacher = User.query.filter(User.name == request.args.get('name')).first()
        #print(str(teacher.teacher_id).zfill(5))
        courses = Course.query.filter(Course.teacher_id == teacher.uid).all()
        #print(courses)
        applications = ModifyApplication.query.filter_by(teacher_id=teacher.teacher_id).order_by(
            ModifyApplication.id.desc()).all()
        for c in courses:
            for i in [0, 7]:
                if (c.time[i] == '0'):
                    break
                else:
                    a[b[int(c.time[i + 2]) - 1] - 1][int(c.time[i + 1])] = c.course_name
                    if (c.time[i] == '3'):
                        a[b[int(c.time[i + 2]) - 1]][int(c.time[i + 1])] = c.course_name
                    # a[b[int(c.time[i + 1])]][int(c.time[i + 2])] = c.course_name
                    # if(c.time[i+3]=='3'):
                    #     a[b[int(c.time[i + 1])]+1][int(c.time[i + 2])] = c.course_name
        print(applications)
    return render_template('ClassArrange/teachermain.html', Courses=a, applications=applications)


@bp.route('/department')
@login_required
def department():
    Courses = Course.query.all()
    a = []
    Classrooms = Classroom.query.filter(Classroom.status == 0).all()
    location = []
    for c in Classrooms:
        location.append(c)
    for c in Courses:
        b = []
        Teachers = User.query.filter(User.uid == c.teacher_id).first()
        classroom = Classroom.query.filter(Classroom.id == c.time[4:7] and Classroom.status == 0).first()
        # classroom = location[int(c.time[4:7])]
        print(classroom)
        b.append(c.cid)
        b.append(c.name)
        try:
            b.append(Teachers.name)
        except:
            pass
        b.append(decoder(c.time))
        try:
            b.append(classroom.location)
        except:
            pass
        a.append(b)
    return render_template('ClassArrange/department.html', Courses=a)


@bp.route('/classroomarrange', methods=['POST', 'GET'])
@login_required
def classroomarrange():
    Classrooms = Classroom.query.filter_by(status=0).all()
    return render_template('ClassArrange/classroomarrange.html', Classrooms=Classrooms)


@bp.route('/connect', methods=['POST', 'GET'])
def connect():
    print(request.form.get("daytime"))
    return "hello"


@bp.route('/deleteclassroom')
@login_required
def deleteclassroom():
    location = request.args.get('location')
    db = get_db()
    classroom = Classroom.query.filter_by(location=location, status=0).first()
    print('fasa')
    all = Course.query.filter().all()
    # + TermCourse.query.filter(TermCourse.time[11:14] == classroom.id).count()
    # db.session.delete(classroom)
    num = 0
    for a in all:
        if a.time[4:7] == classroom.id or (a.time[7] != '0' and a.time[11:14] == classroom.id):
            num += 1
    if num == 0:
        classroom.status = 1
        classroom.location = classroom.location + "(deleted)"
        try:
            db.session.commit()
            error = "成功删除教室：「" + classroom.location + "」"
        except:
            db.session.rollback()
            error = "删除失败！"
        print(classroom.location)
        # flash("成功删除教室：" + clƒassroom.location)
    else:
        error = "删除失败，有课程与该教室关联!"
    flash(error)
    return redirect(url_for('classarrange.classroomarrange'))


@bp.route('/classroommodify', methods=['POST', 'GET'])
@login_required
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


#
# @bp.route('/classroommodify', methods=['POST', 'GET'])
# def classroommodify():
#     if request.method == 'POST':
#         error = "修改失败！"
#         campus = request.form['campus']
#         location = request.form['location']
#         capacity = request.form['capacity']
#         classroom = Classroom.query.filter_by(location=location, status=0).first()
#         if campus:
#             classroom.campus = campus
#         if capacity:
#             print("capacity")
#             print(capacity)
#             classroom.capacity = int(capacity)
#         db = get_db()
#         db.session.add(classroom)
#         print(db.session.commit())
#         # if db.session.commit():
#         error = '修改成功!'
#         flash(error)
#     return redirect(url_for('classarrange.classroomarrange'))


@bp.route('/showroom', methods=['POST', 'GET'])
@login_required
def showroom():
    return render_template('ClassArrange/class_schedule.html')


@bp.route('/application', methods=['POST', 'GET'])
@login_required
def application():
    applications = ModifyApplication.query.filter_by().all()
    return render_template('ClassArrange/application.html', apply=applications)


# @bp.route('/teachermain', methods=['POST', 'GET'])
# def teachermain():
#     return render_template('teachermain.html')
@bp.route('/teacher_schedule', methods=['POST', 'GET'])
@login_required
def teacher_schedule():
    application = ModifyApplication.query.filter_by(teacher_id=current_user.id)
    return render_template('ClassArrange/teacher_schedule.html', application=application)


@bp.route('/add', methods=['POST', 'GET'])
@login_required
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
    return redirect(url_for('classarrange.classroomarrange'))


@bp.route('/muladd', methods=['POST', 'GET'])
@login_required
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
            flash("文件 %s 中没有内容！") % file.filename
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
                db.session.rollback()
                error = "添加失败！"
                flag = False
                break
        flash(error)
    # # return redirect(url_for('library.addbook'))
    return redirect(url_for('classarrange.classroomarrange'))


def uploaded_file(filename):
    return send_from_directory(filename)


# @bp.route('/allclassroom', methods=['POST', 'GET'])
# def allclassroom():
#     return render_template('classroomarrange.html')


@bp.route('/query', methods=['POST', 'GET'])
@login_required
def query():
    # urls = "ClassArrange/department"
    if request.method == 'POST':
        location = request.form['location']

        error = None
        if location is None:
            flash("请输入查询条件 ！")
        else:
            classroom = Classroom.query.filter_by(location=location).first()
            if not classroom:
                flash("教室不存在！")
                print(classroom)
                return redirect(url_for('classarrange.teacher_schedule'))
        a = []
        period = ["08:00~09:35", "09:50~11:25", "11:30~12:15", "13:15~14:50",
                  "14:55~15:40", "15:55~17:30", "18:30~20:05", "20:10~20:55"]
        for i in range(8):
            tmp = [period[i]]
            for j in range(5):
                tmp.append(" ")
            a.append(tmp)
        b = [1, 2, 4, 6, 7]  # 221 212 21
        #teacher = User.query.filter().first()
        teacher = User.query.filter(User.status == "教师").first()
        courses = Course.query.filter().all()
        Classrooms = Classroom.query.filter(Classroom.status == 0).all()
        location = []
        for c in Classrooms:
            location.append(c)
        for c in courses:
            for i in [0, 7]:
                if c.time[i] == '0':
                    break
                else:
                    classroom = Classroom.query.filter(
                        Classroom.id == c.time[i + 4:i + 7] and Classroom.status == 0).first()
                    # classroom = location[int(c.time[i + 4:i + 7])]
                    print(classroom.location)
                    if classroom.location == request.form['location']:
                        a[b[int(c.time[i + 2]) - 1] - 1][int(c.time[i + 1])] = c.course_name
                        if (c.time[i] == "3"):
                            a[b[int(c.time[i + 2]) - 1]][int(c.time[i + 1])] = c.course_name
        print(a)
        return render_template('ClassArrange/class_schedule.html', tables=a)


@bp.route('/delete', methods=['POST', 'GET'])
@login_required
@bp.before_app_request
def load_logged_in_query():
    query = session.get('query')
    if query is None:
        g.query = None
    else:
        g.query = query
        print(g.query)


# @bp.route('/deleteclassroom', methods=('GET',))
# # @login_required
# def deleteclassroom():
#     location = request.args.get('location')
#     db = get_db()
#     classroom = Classroom.query.filter(Classroom.location == location).first()
#     db.session.delete(classroom)
#     if not (db.session.commit()):
#         error = '无法删除！'
#         flag = False
#     classrooms = Classroom.query.all()
#     if flag is False:
#         flash(error)
#     else:
#         flash("成功删除教室：" + classroom.location)
#     return render_template('department.html', classrooms=classrooms)


@bp.route('/autorange', methods=['POST', 'GET'])
@login_required
def autoarrange(bd="紫金港"):
    print('gf8888')
    # flash("删除成功")
    error = "排课成功！"
    import random

    dic = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 2, 0], [0, 1, 1]]
    n = Classroom.query.filter(Classroom.campus == bd and Classroom.status == 0).count()
    m = User.query.filter(User.status == "教师").count()

    list2 = [0] * 10
    list3 = [0] * 15
    sum2 = 0
    sum3 = 0
    for i in range(10):
        list2[i] = n
        sum2 += n
    for i in range(15):
        list3[i] = n
        sum3 += n

    C2 = [0] * m
    C3 = [0] * m

    Class2 = [0] * m
    Class3 = [0] * m

    Use2 = [0] * m
    Use3 = [0] * m

    Arr2 = [[0 for i in range(30)] for i in range(m)]
    Cls2 = [[0 for i in range(30)] for i in range(m)]
    Arr3 = [[0 for i in range(30)] for i in range(m)]
    Cls3 = [[0 for i in range(30)] for i in range(m)]

    teacher = User.query.filter(User.status == "教师").all()
    for i, t in enumerate(teacher):
        print('hgj')
        course = Course.query.filter(Course.teacher_id == t.uid ).all()
        # Class2[i], Class3[i] = map(int, input().split())
        Class2[i], Class3[i] = 0, 0
        for j, c in enumerate(course):
            #print(teacher.name, course.name)
            Class2[i] += dic[c.credit][1]
            Class3[i] += dic[c.credit][2]
            # fuckk
        C2[i] = Class2[i]
        C3[i] = Class3[i]
        Use2[i] = Use3[i] = 0
    flag = 0

    print('!!!')
    Ruse = [0] * 20
    for i in range(m):
        p = Class2[i]
        Class2[i] = max(0, Class2[i] - 10, Class2[i] - sum2)
        sum2 -= p - Class2[i]
        for j in range(10):
            Ruse[j] = 0
        for j in range(p - Class2[i]):
            for k in range(10):

                if not Ruse[k]:
                    mx = list2[k]
                    break
            for k in range(10):
                if list2[k] > mx and not Ruse[k]: mx = list2[k]
            cnt = 0
            for k in range(10):
                if list2[k] == mx and not Ruse[k]: cnt += 1
            R = random.randint(1, cnt)
            v = 0
            for k in range(10):
                if list2[k] == mx and not Ruse[k]:
                    v += 1
                if v == R:
                    Arr2[i][Use2[i]] = k
                    Ruse[k] = 1
                    Cls2[i][Use2[i]] = list2[k]
                    list2[k] -= 1
                    break
            Use2[i] += 1
    print(list2[8])
    for i in range(m):
        p = Class3[i]
        Class3[i] = max(0, Class3[i] - 15, Class3[i] - sum3)
        sum3 -= p - Class3[i]
        for j in range(15):
            Ruse[j] = 0
        for j in range(p - Class3[i]):
            for k in range(15):
                if not Ruse[k]:
                    mx = list3[k]
                    break
            for k in range(15):
                if list3[k] > mx and not Ruse[k]: mx = list3[k]
            cnt = 0
            for k in range(15):
                if list3[k] == mx and not Ruse[k]: cnt += 1
            R = random.randint(1, cnt)
            v = 0
            for k in range(15):
                if list3[k] == mx and not Ruse[k]:
                    v += 1
                if v == R:
                    ##print(i,Use3[i])
                    Arr3[i][Use3[i]] = k + 10
                    Cls3[i][Use3[i]] = list3[k]
                    list3[k] -= 1
                    break
            Use3[i] += 1

    # for i in range(m):
    #     p = Class2[i]
    #     Class2[i] = max(0, Class2[i] - 15, Class2[i] - sum3)
    #     sum3 -= p - Class2[i]
    #     for j in range(15):
    #         Ruse[j] = 0
    #     for j in range(p - Class2[i]):
    #         for k in range(15):
    #             if not Ruse[k]:
    #                 mx = list3[k]
    #                 break
    #         for k in range(15):
    #             if list3[k] > mx and not Ruse[k]: mx = list3[k]
    #         cnt = 0
    #         for k in range(15):
    #             if list3[k] == mx and not Ruse[k]: cnt += 1
    #         R = random.randint(1, cnt)
    #         v = 0
    #         for k in range(15):
    #             if list3[k] == mx and not Ruse[k]:
    #                 v += 1
    #             if v == R:
    #                 Arr2[i][Use2[i]] = k + 10
    #                 Cls2[i][Use2[i]] = list3[k]
    #                 list3[k] -= 1
    #                 break
    #         Use2[i] += 1
    Day = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5]
    Time = [1, 4, 1, 4, 1, 4, 1, 4, 1, 4, 2, 3, 5, 2, 3, 5, 2, 3, 5, 2, 3, 5, 2, 3, 5]

    shuf = [[0 for i in range(n)] for i in range(25)]

    for T in range(25):
        for i in range(n):
            shuf[T][i] = i + 1
    ## shuf[i][j]的意思是 i时段 j号教室实际上应该是shuf[i][j]教室
    for T in range(25):
        random.shuffle(shuf[T])

    for i, t in enumerate(teacher):
        if (Class2[i] > 0):
            # flash("ERROR")
            error = "排课失败"
        if (Class3[i] > 0):
            # flash("ERROR")
            error = "排课失败"
        print(i)
        k, v = 0, 0
        course = Course.query.filter(Course.teacher_id == t.uid).all()
        print(course, "fsfjsfnsjnfskjfn")
        for j, c in enumerate(course):
            print(c.name)
            tmp = ["0" for i in range(14)]
            print('fuck', c.credit, 'hhhh')
            # 一共14位，假设每个课程最多有两时间阶段，也就是前七位和后七位，
            # 因此单独分析七位即可，0000000代表该时间段无课程，
            # 第一位代表课时，第二位代表周几（1-5），第三位代表每天的时间段（1-5，按照23323划分一天），
            # 第四位代表校区，后三位代表教室编号
            bid = 0
            k = j
            if c.credit == 2:
                tmp[0] = str(2)
                tmp[1] = str(Day[Arr2[i][k]])
                tmp[2] = str(Time[Arr2[i][k]])
                tmp[3] = str(bid)
                tmp[4] = str(shuf[Arr2[i][k]][Cls2[i][k] - 1] // 100)
                tmp[5] = str((shuf[Arr2[i][k]][Cls2[i][k] - 1] // 10) % 10)
                tmp[6] = str(shuf[Arr2[i][k]][Cls2[i][k] - 1] % 10)
                k += 1
                print('azzz', tmp)
            elif c.credit == 3:
                tmp[0] = str(3)
                tmp[1] = str(Day[Arr3[i][v]])
                tmp[2] = str(Time[Arr3[i][v]])
                tmp[3] = str(bid)
                tmp[4] = str(shuf[Arr3[i][k]][Cls3[i][k] - 1] // 100)
                tmp[5] = str((shuf[Arr3[i][k]][Cls3[i][k] - 1] // 10) % 10)
                tmp[6] = str(shuf[Arr3[i][k]][Cls3[i][k] - 1] % 10)
                v += 1
                print('sbsbs',tmp)
            elif c.credit == 4:
                tmp[0] = str(2)
                tmp[1] = str(Day[Arr2[i][k]])
                tmp[2] = str(Time[Arr2[i][k]])
                tmp[3] = str(bid)
                tmp[4] = str(shuf[Arr2[i][k]][Cls2[i][k] - 1] // 100)
                tmp[5] = str((shuf[Arr2[i][k]][Cls2[i][k] - 1] // 10) % 10)
                tmp[6] = str(shuf[Arr2[i][k]][Cls2[i][k] - 1] % 10)
                k += 1

                tmp[7] = str(2)
                tmp[8] = str(Day[Arr2[i][k]])
                tmp[9] = str(Time[Arr2[i][k]])
                tmp[10] = str(bid)
                tmp[11] = str(shuf[Arr2[i][k]][Cls2[i][k] - 1] // 100)
                tmp[12] = str((shuf[Arr2[i][k]][Cls2[i][k] - 1] // 10) % 10)
                tmp[13] = str(shuf[Arr2[i][k]][Cls2[i][k] - 1] % 10)
                k += 1
            elif c.credit == 5:
                tmp[0] = str(2)
                tmp[1] = str(Day[Arr2[i][k]])
                tmp[2] = str(Time[Arr2[i][k]])
                tmp[3] = str(bid)
                tmp[4] = str(shuf[Arr2[i][k]][Cls2[i][k] - 1] // 100)
                tmp[5] = str((shuf[Arr2[i][k]][Cls2[i][k] - 1] // 10) % 10)
                tmp[6] = str(shuf[Arr2[i][k]][Cls2[i][k] - 1] % 10)
                k += 1

                tmp[7] = str(3)
                tmp[8] = str(Day[Arr3[i][v]])
                tmp[9] = str(Time[Arr3[i][v]])
                tmp[10] = str(bid)
                tmp[11] = str(shuf[Arr2[i][k]][Cls2[i][k] - 1] // 100)
                tmp[12] = str((shuf[Arr2[i][k]][Cls2[i][k] - 1] // 10) % 10)
                tmp[13] = str(shuf[Arr2[i][k]][Cls2[i][k] - 1] % 10)
                v += 1
            Class2[i] += dic[c.credit][1]
            Class3[i] += dic[c.credit][2]
            print('rnm')
            if tmp[8] != "0" and (int(tmp[1]) > int(tmp[8]) or int(tmp[1]) == int(tmp[8]) and int(tmp[2]) > int(tmp[9])):
                tmp[0:7], tmp[7:14] = tmp[7:14], tmp[0:7]
            c.time = ''.join(tmp)
            print('tuiqian')

    db = get_db()
    db.session.commit()
    Courses = Course.query.all()
    print('bnm')
    a = []
    Classrooms = Classroom.query.filter(Classroom.status == 0).all()
    location = []
    for c in Classrooms:
        location.append(c.location)
        print(c.location)
    for c in Courses:
        print('gdsg')
        b = []
        Teachers = User.query.filter(User.uid == c.teacher_id).first()
        # Classrooms = Classroom.query.filter(Classroom.id == c.time[4:7] and Classroom.status == 0).first()
        b.append(c.cid)
        b.append(c.name)
        b.append(Teachers.name)
        b.append(decoder(c.time))
        b.append(location[int(c.time[4:7])])
        a.append(b)
    flash(error)
    return redirect(url_for('classarrange.department'))
    # return render_template('department.html', Courses=a)
    # return render_template('department.html', Courses=Courses)


# @bp.route('/TeacherCourse', methods=['POST', 'GET'])
# def TeacherCourse():
#     if request.method == 'POST':
#
#         a = []
#         Courses = TermCourse.filter(TermCourse.teacher_id == request.form['id']).all()
#
#     return render_template('department.html', Courses=a)
@bp.route('/TeacherCourse', methods=['POST', 'GET'])
@login_required
def TeacherCourse():
    a = []
    period = ["08:00~09:35", "09:50~11:25", "11:30~12:15", "13:15~14:50",
              "14:55~15:40", "15:55~17:30", "18:30~20:05", "20:10~20:55"]
    for i in range(8):
        tmp = [period[i]]
        for j in range(5):
            tmp.append(" ")
        a.append(tmp)
    b = [1, 2, 4, 6, 7]  # 221 212 21
    teacher = User.query.filter(User.name == request.args.get('name')).first()
    print(teacher)
    if not teacher:
        teacher = User.query.filter(User.uid == current_user.uid).first()
        applications = ModifyApplication.query.filter_by(teacher_id=teacher.uid).all()
    print(teacher)
    name = teacher.name
    error = None
    if teacher:
        #print(str(teacher.teacher_id).zfill(5))
        courses = Course.query.filter(Course.teacher_id == teacher.uid).all()
        print(courses)
        applications = ModifyApplication.query.filter_by(teacher_id=teacher.uid).order_by(
            ModifyApplication.id.desc()).all()
        for c in courses:
            for i in [0, 7]:
                if (c.time[i] == '0'):
                    break
                else:
                    a[b[int(c.time[i + 2]) - 1] - 1][int(c.time[i + 1])] = c.name
                    if (c.time[i] == '3'):
                        a[b[int(c.time[i + 2]) - 1]][int(c.time[i + 1])] = c.name
                    # a[b[int(c.time[i + 1])]][int(c.time[i + 2])] = c.course_name
                    # if(c.time[i+3]=='3'):
                    #     a[b[int(c.time[i + 1])]+1][int(c.time[i + 2])] = c.course_name
        print(applications)
    return render_template('ClassArrange/teachermain.html', Courses=a, applications=applications)


@bp.route('/submitapply', methods=['POST', 'GET'])
@login_required
def submitapply():
    if request.method == 'POST':
        error = None
        # *********************************这里要用教师名！！！！*****************************************#
        teacher_id = current_user.uid
        # *********************************这里要用教师名！！！！*****************************************#

        content = request.form['content']
        # 0:未处理 1：处理完成 2：被拒绝
        statecode = 0
        if len(content) > 200:
            error = "字数超过上限！"
        elif content is None:
            error = "未填写内容！"
        else:
            applcation = ModifyApplication(teacher_id=teacher_id, content=content, statecode=statecode)
            db = get_db()
            db.session.add(applcation)
            db.session.commit()
            error = "提交申请成功"
        flash(error)
    return redirect(url_for('classarrange.TeacherCourse'))


@bp.route('/processapplication', methods=['POST', 'GET'])
@login_required
def processapplication():
    if request.method == 'POST':
        # *********************************这里要用教师名！！！！*****************************************#
        id = request.form['id']
        # *********************************这里要用教师名！！！！*****************************************#
        # content = request.form['content']
        statecode = request.form['statecode']
        # *********************************这里要用管理员名！！！！*****************************************#
        handler = current_user.uid
        # *********************************这里要用管理员名！！！！*****************************************#

        application = ModifyApplication.query.filter_by(id=id).first()
        if application is not None:
            application.statecode = statecode
            application.handler = handler
            db = get_db()
            db.session.add(application)
            db.session.commit()
            error = "处理成功！"
        else:
            error = "处理失败！"
        flash(error)
    return redirect(url_for('classarrange.application'))


@bp.route('/prints')
@login_required
def prints():
    import pandas as pd
    a = []
    period = ["08:00~09:35", "09:50~11:25", "11:30~12:15", "13:15~14:50",
              "14:55~15:40", "15:55~17:30", "18:30~20:05", "20:10~20:55"]
    for i in range(8):
        tmp = [period[i]]
        for j in range(5):
            tmp.append(" ")
        a.append(tmp)
    b = [1, 2, 4, 6, 7]  # 221 212 21

    error = None
    if not request.args.get('name'):
        error = 'name is required'
        flash(error)
    else:
        teacher = User.query.filter(User.name == request.args.get('name')).first()
        courses = Course.query.filter(Course.teacher_id == teacher.uid).all()
        for c in courses:
            for i in [0, 7]:
                if (c.time[i] == '0'):
                    break
                else:
                    a[b[int(c.time[i + 2]) - 1] - 1][int(c.time[i + 1])] = c.course_name
                    if (c.time[i] == '3'):
                        a[b[int(c.time[i + 2]) - 1]][int(c.time[i + 1])] = c.course_name
                    # a[b[int(c.time[i + 1])]][int(c.time[i + 2])] = c.course_name
                    # if(c.time[i+3]=='3'):
                    #     a[b[int(c.time[i + 1])]+1][int(c.time[i + 2])] = c.course_name
        print(a)
        df = pd.DataFrame(a, columns=["time", "周一", "周二", "周三", "周四", "周五"])
        df.to_csv("hhh.csv", index=False)
    return redirect(url_for('classarrange.teachermain'))


@bp.route('/printtable', methods=['POST'])
@login_required
def printtable():
    import pandas as pd
    a = []
    period = ["08:00~09:35", "09:50~11:25", "11:30~12:15", "13:15~14:50",
              "14:55~15:40", "15:55~17:30", "18:30~20:05", "20:10~20:55"]
    for i in range(8):
        tmp = [period[i]]
        for j in range(5):
            tmp.append(" ")
        a.append(tmp)
    b = [1, 2, 4, 6, 7]  # 221 212 21
    application = ModifyApplication.query.filter_by().order_by(ModifyApplication.id.desc()).all()
    error = None
    # if not g.name:
    if not current_user.uid:
        error = 'name is required'
        flash(error)
    else:
        try:
            teacher = User.query.filter(User.uid == current_user.uid).first()
            # teacher = Teacher.query.filter(Teacher.teacher_name == request.args.get('name')).first()
            courses = Course.query.filter(Course.teacher_id == teacher.uid).all()
        except:
            flash('fuck')
            return redirect(url_for('classarrange.TeacherCourse'))
        for c in courses:
            for i in [0, 7]:
                if (c.time[i] == '0'):
                    break
                else:
                    a[b[int(c.time[i + 2]) - 1] - 1][int(c.time[i + 1])] = c.name
                    if (c.time[i] == '3'):
                        a[b[int(c.time[i + 2]) - 1]][int(c.time[i + 1])] = c.name
                    # a[b[int(c.time[i + 1])]][int(c.time[i + 2])] = c.course_name
                    # if(c.time[i+3]=='3'):
                    #     a[b[int(c.time[i + 1])]+1][int(c.time[i + 2])] = c.course_name
        print(a)
        df = pd.DataFrame(a, columns=["time", "周一", "周二", "周三", "周四", "周五"])
        # df.to_csv("ClassSchedule.csv", index=False)
        df.to_csv("教师课表.csv", index=False)
        # df.to_csv(g.name + "csv", index=False)
        flash("打印成功！")
    return redirect(url_for('classarrange.TeacherCourse'))
    # return render_template('ClassArrange/teachermain.html', Courses=a)

# import datetime
# import functools
# # from flask_filer import FileField, FileRequired, FileAllowed
# import os.path
# import time
#
# import xlrd
# from flask_login import login_required, current_user
# from sqlalchemy import or_, and_, text
# # from openpyxl import load_workbook
# from flask import send_from_directory
# from flask import (
#     current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for
# )
# from flask import send_from_directory
# import xlrd
# from sqlalchemy.orm import sessionmaker
# from werkzeug.security import check_password_hash, generate_password_hash
# from werkzeug.utils import secure_filename
# from xlrd import open_workbook
# from xlrd.timemachine import xrange
#
# from werkzeug.exceptions import abort
# # from uploads import ALLOWED_EXTENSIONS
# # from user import login_required
# import classarrange
# from database import get_db
#
# # import pandas as pd
#
# UPLOAD_FOLDER = 'uploads'
# bp = Blueprint('classarrange', __name__, url_prefix='/classarrange')
# # from models import Application,Classroom,Course,Teacher,TermCourse
#
# # bp = Blueprint('classarrange', __name__, url_prefix='/classarrange')
# from models import Classroom, TermCourse, Teacher, ModifyApplication
#
#
# @bp.route('/')
# def hello_world():
#     return render_template('sidebar.html')
#
#
# @bp.route('/hello')
# def test():
#     print("a")
#     return "Hello"
#
#
# @bp.route('/class_schedule')
# @login_required
# def class_schedule():
#     a = []
#     period = ["08:00~09:35", "09:50~11:25", "11:30~12:15", "13:15~14:50",
#               "14:55~15:40", "15:55~17:30", "18:30~20:05", "20:10~20:55"]
#     for i in range(8):
#         tmp = [period[i]]
#         for j in range(5):
#             tmp.append(" ")
#         a.append(tmp)
#     b = [1, 2, 4, 6, 7]  # 221 212 21
#     teacher = Teacher.query.filter().first()
#     courses = TermCourse.query.filter().all()
#     Classrooms = Classroom.query.filter(Classroom.status == 0).all()
#     location = []
#     for c in Classrooms:
#         location.append(c)
#     for c in courses:
#         for i in [0, 7]:
#             if c.time[i] == '0':
#                 break
#             else:
#                 classroom = Classroom.query.filter(
#                     Classroom.id == c.time[i + 4:i + 7] and Classroom.status == 0).first()
#                 # classroom = location[int(c.time[i + 4:i + 7])]
#                 print(classroom.location)
#                 if classroom.location == request.args.get('name'):
#                     a[b[int(c.time[i + 2]) - 1] - 1][int(c.time[i + 1])] = c.course_name
#                     if (c.time[i] == "3"):
#                         a[b[int(c.time[i + 2]) - 1]][int(c.time[i + 1])] = c.course_name
#     print(a)
#     return render_template('ClassArrange/class_schedule.html', tables=a)
#
#
# def decoder(s):  # 解码器
#     a = [["周一", "周二", "周三", "周四", "周五"], \
#          ["08:00", "09:50", "13:15", "15:55", "18:30"], \
#          ["09:35", "11:25", "14:55", "17:30", "20:05"],
#          ["09:35", "12:15", "15:40", "17:30", "20:55"]]
#     haha = ["", ""]
#     for i in [0, 7]:
#         if s[i] == "0":
#             if i == 7:
#                 haha += "\n"
#             break
#         else:
#             haha[i // 7] += a[0][int(s[i + 1]) - 1] + ":"
#             haha[i // 7] += a[1][int(s[i + 2]) - 1]
#             haha[i // 7] += "-"
#             haha[i // 7] += a[int(s[i])][int(s[i + 2]) - 1]
#
#     return haha
#
#
# @bp.route('/classmodify', methods=['POST', 'GET'])
# @login_required
# def classmodify():
#     period = ["08:00~09:35", "09:50~11:25", "11:30~12:15", "13:15~14:50",
#               "14:55~15:40", "15:55~17:30", "18:30~20:05", "20:10~20:55"]
#     periods = {"0": "1", "1": "2", "2": "2", "3": "3", "4": "3", "5": "4", "6": "5", "7": "5"}
#     daytime = {"周一": 1, "周二": 2, "周三": 3, "周四": 4, "周五": 5}
#     if request.method == 'POST':
#         # oldlocation = request.form['oldloaction']
#
#         print(request)
#         course_name = request.form['name']
#         daytime1 = request.form['daytime1']
#         periods1 = request.form['periods1']
#         daytime2 = request.form['daytime2']
#         periods2 = request.form['periods2']
#         print('gggfsfsfsfsfs')
#         location = request.form['classroom1']
#         print('gggfsfsfs1fsfs')
#         # flash(course_name)
#         # flash(daytime1)
#         # flash(daytime2)
#         # flash(periods1)
#         # pass
#         print('fsfsfsfsfs')
#         classroom = Classroom.query.filter_by(location=location).first()
#         print(classroom.location)
#         ID = classroom.id
#         termCourse = TermCourse.query.filter_by(course_name=course_name).first()
#         # 生成timecode
#         # 一共14位，假设每个课程最多有两时间阶段，也就是前七位和后七位，
#         # 因此单独分析七位即可，0000000代表该时间段无课程，
#         # 第一位代表课时，第二位代表周几（1-5），第三位代表每天的时间段（1-5，按照23323划分一天），
#         # 第四位代表校区，后三位代表教室编号
#         timecode = [termCourse.time[i] for i in range(len(termCourse.time))]
#         if request.form['classroom1']:
#             for i in range(3):
#                 timecode[i + 4] = ID[i]
#                 timecode[i + 11] = ID[i]
#                 print(i)
#         print('hhh', request.form['daytime1'], request.form['daytime2'], request.form['periods1'])
#         if request.form['daytime1']:
#             timecode[1] = str(int(request.form['daytime1']) + 1)
#         if request.form['daytime2']:
#             timecode[1 + 7] = str(int(request.form['daytime2']) + 1)
#         if request.form['periods1']:
#             print(request.form['periods1'])
#             timecode[2] = periods[request.form['periods1']]
#         if request.form['periods2']:
#             timecode[2 + 7] = periods[request.form['periods2']]
#         timecode = ''.join(timecode)
#         print(timecode)
#         termCourse.time = timecode
#
#         db = get_db()
#         db.session.commit()
#
#         error = '修改成功!'
#         flash(error)
#     return redirect(url_for('classarrange.department'))
#     # return render_template('department.html')
#
#
# # def classmodify():
# #     period = ["08:00~09:35", "09:50~11:25", "11:30~12:15", "13:15~14:50",
# #               "14:55~15:40", "15:55~17:30", "18:30~20:05", "20:10~20:55"]
# #     if request.method == 'POST':
# #         # oldlocation = request.form['oldloaction']
# #
# #         print(request)
# #         course_name = request.form['name']
# #         daytime1 = request.form['daytime1']
# #         periods1 = request.form['periods1']
# #         daytime2 = request.form['daytime2']
# #         periods2 = request.form['periods2']
# #         print('gggfsfsfsfsfs')
# #         location = request.form['classroom1']
# #         print('gggfsfsfs1fsfs')
# #         # flash(course_name)
# #         # flash(daytime1)
# #         # flash(daytime2)
# #         # flash(periods1)
# #         # pass
# #         print('fsfsfsfsfs')
# #         classroom = Classroom.query.filter_by(location=location).first()
# #         print(classroom.location)
# #         ID = classroom.id
# #         termCourse = TermCourse.query.filter_by(course_name=course_name).first()
# #         # 生成timecode
# #         # 一共14位，假设每个课程最多有两时间阶段，也就是前七位和后七位，
# #         # 因此单独分析七位即可，0000000代表该时间段无课程，
# #         # 第一位代表课时，第二位代表周几（1-5），第三位代表每天的时间段（1-5，按照23323划分一天），
# #         # 第四位代表校区，后三位代表教室编号
# #         timecode = [termCourse.time[i] for i in range(len(termCourse.time))]
# #         if request.form['classroom1']:
# #             pass
# #             for i in range(3):
# #                 timecode[i + 4] = ID[i]
# #                 timecode[i + 11] = ID[i]
# #                 print(i)
# #             timecode = ''.join(timecode)
# #             print(timecode)
# #         if periods1:
# #             pass
# #             timecode
# #         if periods2:
# #             pass
# #             timecode
# #         termCourse.time = timecode
# #
# #         db = get_db()
# #         db.session.commit()
# #
# #         error = '修改成功!'
# #         flash(error)
# #     return redirect(url_for('classarrange.department'))
# #     # return render_template('department.html')
# @login_required
# def homepage():
#     a = []
#     period = ["08:00~09:35", "09:50~11:25", "11:30~12:15", "13:15~14:50",
#               "14:55~15:40", "15:55~17:30", "18:30~20:05", "20:10~20:55"]
#     for i in range(8):
#         tmp = [period[i]]
#         for j in range(5):
#             tmp.append(" ")
#         a.append(tmp)
#     b = [1, 2, 4, 6, 7]  # 221 212 21
#     teacher = Teacher.query.filter(Teacher.teacher_name == g['name']).first()
#     print(teacher)
#     if not teacher:
#         teacher = Teacher.query.filter(Teacher.teacher_id == current_user.uid).first()
#         applications = ModifyApplication.query.filter_by(teacher_id=teacher.teacher_id).all()
#
#     name = teacher.teacher_name
#     error = None
#     if teacher:
#         teacher = Teacher.query.filter(Teacher.teacher_name == request.args.get('name')).first()
#         print(str(teacher.teacher_id).zfill(5))
#         courses = TermCourse.query.filter(TermCourse.teacher_id == str(teacher.teacher_id).zfill(5)).all()
#         print(courses)
#         applications = ModifyApplication.query.filter_by(teacher_id=teacher.teacher_id).order_by(
#             ModifyApplication.id.desc()).all()
#         for c in courses:
#             for i in [0, 7]:
#                 if (c.time[i] == '0'):
#                     break
#                 else:
#                     a[b[int(c.time[i + 2]) - 1] - 1][int(c.time[i + 1])] = c.course_name
#                     if (c.time[i] == '3'):
#                         a[b[int(c.time[i + 2]) - 1]][int(c.time[i + 1])] = c.course_name
#                     # a[b[int(c.time[i + 1])]][int(c.time[i + 2])] = c.course_name
#                     # if(c.time[i+3]=='3'):
#                     #     a[b[int(c.time[i + 1])]+1][int(c.time[i + 2])] = c.course_name
#         print(applications)
#     return render_template('ClassArrange/teachermain.html', Courses=a, applications=applications)
#
#
# @bp.route('/department')
# @login_required
# def department():
#     Courses = TermCourse.query.all()
#     a = []
#     Classrooms = Classroom.query.filter(Classroom.status == 0).all()
#     location = []
#     for c in Classrooms:
#         location.append(c)
#     for c in Courses:
#         b = []
#         Teachers = Teacher.query.filter(Teacher.teacher_id == c.teacher_id).first()
#         classroom = Classroom.query.filter(Classroom.id == c.time[4:7] and Classroom.status == 0).first()
#         # classroom = location[int(c.time[4:7])]
#         b.append(c.course_id)
#         b.append(c.course_name)
#         b.append(Teachers.teacher_name)
#         b.append(decoder(c.time))
#         b.append(classroom.location)
#         a.append(b)
#     return render_template('ClassArrange/department.html', Courses=a)
#
#
# @bp.route('/classroomarrange', methods=['POST', 'GET'])
# @login_required
# def classroomarrange():
#     Classrooms = Classroom.query.filter_by(status=0).all()
#     return render_template('ClassArrange/classroomarrange.html', Classrooms=Classrooms)
#
#
# @bp.route('/connect', methods=['POST', 'GET'])
# def connect():
#     print(request.form.get("daytime"))
#     return "hello"
#
#
# @bp.route('/deleteclassroom')
# @login_required
# def deleteclassroom():
#     location = request.args.get('location')
#     db = get_db()
#     classroom = Classroom.query.filter_by(location=location, status=0).first()
#     print('fasa')
#     all = TermCourse.query.filter().all()
#     # + TermCourse.query.filter(TermCourse.time[11:14] == classroom.id).count()
#     # db.session.delete(classroom)
#     num = 0
#     for a in all:
#         if a.time[4:7] == classroom.id or (a.time[7] != '0' and a.time[11:14] == classroom.id):
#             num += 1
#     if num == 0:
#         classroom.status = 1
#         classroom.location = classroom.location + "(deleted)"
#         try:
#             db.session.commit()
#             error = "成功删除教室：「" + classroom.location + "」"
#         except:
#             db.session.rollback()
#             error = "删除失败！"
#         print(classroom.location)
#         # flash("成功删除教室：" + clƒassroom.location)
#     else:
#         error = "删除失败，有课程与该教室关联!"
#     flash(error)
#     return redirect(url_for('classarrange.classroomarrange'))
#
#
# @bp.route('/classroommodify', methods=['POST', 'GET'])
# @login_required
# def classroommodify():
#     if request.method == 'POST':
#         error = None
#         capacity = request.form['capacity']
#         location = request.form['location']
#         campus = request.form['campus']
#         classroom = Classroom.query.filter_by(location=location, status=0).first()
#         if capacity:
#             if int(capacity) <= 0:
#                 error = "修改容量不能小于等于0！"
#             elif int(capacity) > 500:
#                 error = "教室容量不能超过500人！"
#             else:
#                 classroom.capacity = capacity
#                 db = get_db()
#                 try:
#                     db.session.commit()
#                     error = "修改教室 " + location + " 容量为：「" + capacity + "」"
#                 except:
#                     db.session.rollback()
#                     return '修改出错！'
#         if error:
#             flash(error)
#     return redirect(url_for('classarrange.classroomarrange'))
#
#
# #
# # @bp.route('/classroommodify', methods=['POST', 'GET'])
# # def classroommodify():
# #     if request.method == 'POST':
# #         error = "修改失败！"
# #         campus = request.form['campus']
# #         location = request.form['location']
# #         capacity = request.form['capacity']
# #         classroom = Classroom.query.filter_by(location=location, status=0).first()
# #         if campus:
# #             classroom.campus = campus
# #         if capacity:
# #             print("capacity")
# #             print(capacity)
# #             classroom.capacity = int(capacity)
# #         db = get_db()
# #         db.session.add(classroom)
# #         print(db.session.commit())
# #         # if db.session.commit():
# #         error = '修改成功!'
# #         flash(error)
# #     return redirect(url_for('classarrange.classroomarrange'))
#
#
# @bp.route('/showroom', methods=['POST', 'GET'])
# @login_required
# def showroom():
#     return render_template('ClassArrange/class_schedule.html')
#
#
# @bp.route('/application', methods=['POST', 'GET'])
# @login_required
# def application():
#     applications = ModifyApplication.query.filter_by().all()
#     return render_template('ClassArrange/application.html', apply=applications)
#
#
# # @bp.route('/teachermain', methods=['POST', 'GET'])
# # def teachermain():
# #     return render_template('teachermain.html')
# @bp.route('/teacher_schedule', methods=['POST', 'GET'])
# @login_required
# def teacher_schedule():
#     application = ModifyApplication.query.filter_by(teacher_id=current_user.id)
#     return render_template('ClassArrange/teacher_schedule.html', application=application)
#
#
# @bp.route('/add', methods=['POST', 'GET'])
# @login_required
# def add():
#     # form1 = Form1()
#     # form2 = Form2()
#     if request.method == 'POST':
#         print(request.values)
#         # if form1.submit1.data and form1.validate():
#         location = request.form['location']
#         print(location)
#         capacity = request.form['capacity']
#         campus = request.form['campus']
#         db = get_db()
#         error = None
#         if not location:
#             error = '缺少教室名称！'
#         elif not capacity:
#             error = '缺少教室容量'
#         elif int(capacity) <= 0:
#             error = "修改容量不能小于等于0！"
#         elif int(capacity) > 500:
#             error = "教室容量不能超过500人！"
#         elif not campus:
#             error = '缺少校区'
#         if error is None:
#             room = Classroom.query.filter_by(location=location, status=0).first()
#             if room is not None:
#                 error = "已经存在该教室！"
#             else:
#                 n = Classroom.query.filter_by(status=0).count()
#                 id = str(n + 1).zfill(3)
#                 classroom = Classroom(location=location, capacity=capacity, campus=campus, id=id, status=0)
#                 try:
#                     db.session.add(classroom)
#                     db.session.commit()
#                     error = '添加教室:「' + location + "」成功!"
#                 except:
#                     error = "添加教室失败！"
#             print(error)
#             # return redirect(url_for('classarrange.classroomarrange'))
#             # return render_template('classroomarrange.html', error=error, Classroom=Classroom)
#         flash(error)
#     # Classrooms = Classroom.query.all()
#     return redirect(url_for('classarrange.classroomarrange'))
#
#
# @bp.route('/muladd', methods=['POST', 'GET'])
# @login_required
# def muladd():
#     if request.method == 'POST':
#         print(request.files)
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(url_for('classarrange.classroomarrange'))
#         file = request.files['file']
#         bool = file.filename.endswith(".xls")
#         if not bool:
#             flash("上传文件类型必须是 .xls 文件 ！")
#             return redirect(url_for('classarrange.classroomarrange'))
#         print(file.filename)
#         classrooms = xlrd.open_workbook(file_contents=file.read())
#         db = get_db()
#         try:
#             table = classrooms.sheets()[0]
#         except:
#             flash("文件 %s 中没有内容！") % file.filename
#             return redirect(url_for('classarrange.classroomarrange'))
#         nrows = table.nrows
#         ncols = table.ncols
#         names = classrooms.sheet_names()
#         status = classrooms.sheet_loaded(names[0])
#         print(status)
#         # print(os.getcwd(), "nrows %d, ncols %d") % (nrows, ncols)
#         print(nrows)
#         print(ncols)
#         row_list = []
#         error = "成功批量添加："
#         flag = True
#         for i in range(1, nrows):
#             if not flag:
#                 break
#             row_date = table.row_values(i)
#             row_list.append(row_date)
#             print(row_list)
#             n = i - 1
#             print(row_list[n])
#             N = Classroom.query.filter_by(status=0).count()
#             id = str(N + 1).zfill(3)
#             if not row_list[n][0]:
#                 error = "缺少教室所在校区"
#                 flag = False
#             elif not row_list[n][1]:
#                 error = "缺少教室名称"
#                 flag = False
#             elif not row_list[n][2]:
#                 error = "缺少教室容量"
#                 flag = False
#             else:
#                 try:
#                     a = int(row_list[n][2])
#                     if a <= 0:
#                         error = "教室容量不得小于等于0！"
#                         flag = False
#                     elif a > 500:
#                         error = "教室容量不得大于500！"
#                         flag = False
#                 except:
#                     error = "格式错误！"
#                     flag = False
#
#             classroom = Classroom(campus=row_list[n][0], location=row_list[n][1], capacity=row_list[n][2], id=id,
#                                   status=0)
#             try:
#                 db.session.add(classroom)
#                 error = error + "「" + str(row_list[n][1]) + "」"
#                 print(classroom)
#                 db.session.commit()
#             except:
#                 db.session.rollback()
#                 error = "添加失败！"
#                 flag = False
#                 break
#         flash(error)
#     # # return redirect(url_for('library.addbook'))
#     return redirect(url_for('classarrange.classroomarrange'))
#
#
# def uploaded_file(filename):
#     return send_from_directory(filename)
#
#
# # @bp.route('/allclassroom', methods=['POST', 'GET'])
# # def allclassroom():
# #     return render_template('classroomarrange.html')
#
#
# @bp.route('/query', methods=['POST', 'GET'])
# @login_required
# def query():
#     # urls = "ClassArrange/department"
#     if request.method == 'POST':
#         location = request.form['location']
#
#         error = None
#         if location is None:
#             flash("请输入查询条件 ！")
#         else:
#             classroom = Classroom.query.filter_by(location=location).first()
#             if not classroom:
#                 flash("教室不存在！")
#                 print(classroom)
#                 return redirect(url_for('classarrange.teacher_schedule'))
#         a = []
#         period = ["08:00~09:35", "09:50~11:25", "11:30~12:15", "13:15~14:50",
#                   "14:55~15:40", "15:55~17:30", "18:30~20:05", "20:10~20:55"]
#         for i in range(8):
#             tmp = [period[i]]
#             for j in range(5):
#                 tmp.append(" ")
#             a.append(tmp)
#         b = [1, 2, 4, 6, 7]  # 221 212 21
#         teacher = Teacher.query.filter().first()
#         courses = TermCourse.query.filter().all()
#         Classrooms = Classroom.query.filter(Classroom.status == 0).all()
#         location = []
#         for c in Classrooms:
#             location.append(c)
#         for c in courses:
#             for i in [0, 7]:
#                 if c.time[i] == '0':
#                     break
#                 else:
#                     classroom = Classroom.query.filter(
#                         Classroom.id == c.time[i + 4:i + 7] and Classroom.status == 0).first()
#                     # classroom = location[int(c.time[i + 4:i + 7])]
#                     print(classroom.location)
#                     if classroom.location == request.form['location']:
#                         a[b[int(c.time[i + 2]) - 1] - 1][int(c.time[i + 1])] = c.course_name
#                         if (c.time[i] == "3"):
#                             a[b[int(c.time[i + 2]) - 1]][int(c.time[i + 1])] = c.course_name
#         print(a)
#         return render_template('ClassArrange/class_schedule.html', tables=a)
#
#
# @bp.route('/delete', methods=['POST', 'GET'])
# @login_required
# @bp.before_app_request
# def load_logged_in_query():
#     query = session.get('query')
#     if query is None:
#         g.query = None
#     else:
#         g.query = query
#         print(g.query)
#
#
# # @bp.route('/deleteclassroom', methods=('GET',))
# # # @login_required
# # def deleteclassroom():
# #     location = request.args.get('location')
# #     db = get_db()
# #     classroom = Classroom.query.filter(Classroom.location == location).first()
# #     db.session.delete(classroom)
# #     if not (db.session.commit()):
# #         error = '无法删除！'
# #         flag = False
# #     classrooms = Classroom.query.all()
# #     if flag is False:
# #         flash(error)
# #     else:
# #         flash("成功删除教室：" + classroom.location)
# #     return render_template('department.html', classrooms=classrooms)
#
#
# @bp.route('/autorange', methods=['POST', 'GET'])
# @login_required
# def autoarrange(bd="紫金港"):
#     print('gf8888')
#     # flash("删除成功")
#     error = "排课成功！"
#     import random
#
#     dic = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 2, 0], [0, 1, 1]]
#     n = Classroom.query.filter(Classroom.campus == bd and Classroom.status == 0).count()
#     m = Teacher.query.filter().count()
#
#     list2 = [0] * 10
#     list3 = [0] * 15
#     sum2 = 0
#     sum3 = 0
#     for i in range(10):
#         list2[i] = n
#         sum2 += n
#     for i in range(15):
#         list3[i] = n
#         sum3 += n
#
#     C2 = [0] * m
#     C3 = [0] * m
#
#     Class2 = [0] * m
#     Class3 = [0] * m
#
#     Use2 = [0] * m
#     Use3 = [0] * m
#
#     Arr2 = [[0 for i in range(30)] for i in range(m)]
#     Cls2 = [[0 for i in range(30)] for i in range(m)]
#     Arr3 = [[0 for i in range(30)] for i in range(m)]
#     Cls3 = [[0 for i in range(30)] for i in range(m)]
#
#     teacher = Teacher.query.all()
#     for i, t in enumerate(teacher):
#         print('hgj')
#         course = TermCourse.query.filter(TermCourse.teacher_id == t.teacher_id and TermCourse.campus == bd).all()
#         # Class2[i], Class3[i] = map(int, input().split())
#         Class2[i], Class3[i] = 0, 0
#         for j, c in enumerate(course):
#             Class2[i] += dic[c.credit][1]
#             Class3[i] += dic[c.credit][2]
#             # fuckk
#         C2[i] = Class2[i]
#         C3[i] = Class3[i]
#         Use2[i] = Use3[i] = 0
#     flag = 0
#
#     print('!!!')
#     Ruse = [0] * 20
#     for i in range(m):
#         p = Class2[i]
#         Class2[i] = max(0, Class2[i] - 10, Class2[i] - sum2)
#         sum2 -= p - Class2[i]
#         for j in range(10):
#             Ruse[j] = 0
#         for j in range(p - Class2[i]):
#             for k in range(10):
#                 if not Ruse[k]:
#                     mx = list2[k]
#                     break
#             for k in range(10):
#                 if list2[k] > mx and not Ruse[k]: mx = list2[k]
#             cnt = 0
#             for k in range(10):
#                 if list2[k] == mx and not Ruse[k]: cnt += 1
#             R = random.randint(1, cnt)
#             v = 0
#             for k in range(10):
#                 if list2[k] == mx and not Ruse[k]:
#                     v += 1
#                 if v == R:
#                     Arr2[i][Use2[i]] = k
#                     Ruse[k] = 1
#                     Cls2[i][Use2[i]] = list2[k]
#                     list2[k] -= 1
#                     break
#             Use2[i] += 1
#     print(list2[8])
#     for i in range(m):
#         p = Class3[i]
#         Class3[i] = max(0, Class3[i] - 15, Class3[i] - sum3)
#         sum3 -= p - Class3[i]
#         for j in range(15):
#             Ruse[j] = 0
#         for j in range(p - Class3[i]):
#             for k in range(15):
#                 if not Ruse[k]:
#                     mx = list3[k]
#                     break
#             for k in range(15):
#                 if list3[k] > mx and not Ruse[k]: mx = list3[k]
#             cnt = 0
#             for k in range(15):
#                 if list3[k] == mx and not Ruse[k]: cnt += 1
#             R = random.randint(1, cnt)
#             v = 0
#             for k in range(15):
#                 if list3[k] == mx and not Ruse[k]:
#                     v += 1
#                 if v == R:
#                     ##print(i,Use3[i])
#                     Arr3[i][Use3[i]] = k + 10
#                     Cls3[i][Use3[i]] = list3[k]
#                     list3[k] -= 1
#                     break
#             Use3[i] += 1
#
#     for i in range(m):
#         p = Class2[i]
#         Class2[i] = max(0, Class2[i] - 15, Class2[i] - sum3)
#         sum3 -= p - Class2[i]
#         for j in range(15):
#             Ruse[j] = 0
#         for j in range(p - Class2[i]):
#             for k in range(15):
#                 if not Ruse[k]:
#                     mx = list3[k]
#                     break
#             for k in range(15):
#                 if list3[k] > mx and not Ruse[k]: mx = list3[k]
#             cnt = 0
#             for k in range(15):
#                 if list3[k] == mx and not Ruse[k]: cnt += 1
#             R = random.randint(1, cnt)
#             v = 0
#             for k in range(15):
#                 if list3[k] == mx and not Ruse[k]:
#                     v += 1
#                 if v == R:
#                     Arr2[i][Use2[i]] = k + 10
#                     Cls2[i][Use2[i]] = list3[k]
#                     list3[k] -= 1
#                     break
#             Use2[i] += 1
#     Day = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5]
#     Time = [1, 4, 1, 4, 1, 4, 1, 4, 1, 4, 2, 3, 5, 2, 3, 5, 2, 3, 5, 2, 3, 5, 2, 3, 5]
#
#     shuf = [[0 for i in range(n)] for i in range(25)]
#
#     for T in range(25):
#         for i in range(n):
#             shuf[T][i] = i + 1
#     ## shuf[i][j]的意思是 i时段 j号教室实际上应该是shuf[i][j]教室
#     for T in range(25):
#         random.shuffle(shuf[T])
#
#     for i, t in enumerate(teacher):
#         if (Class2[i] > 0):
#             # flash("ERROR")
#             error = "排课失败"
#         if (Class3[i] > 0):
#             # flash("ERROR")
#             error = "排课失败"
#         print(i)
#         k, v = 0, 0
#         course = TermCourse.query.filter(TermCourse.teacher_id == t.teacher_id).all()
#         print(course, "fsfjsfnsjnfskjfn")
#         for j, c in enumerate(course):
#             tmp = ["0" for i in range(14)]
#             print('fuck', c.credit, 'hhhh')
#             # 一共14位，假设每个课程最多有两时间阶段，也就是前七位和后七位，
#             # 因此单独分析七位即可，0000000代表该时间段无课程，
#             # 第一位代表课时，第二位代表周几（1-5），第三位代表每天的时间段（1-5，按照23323划分一天），
#             # 第四位代表校区，后三位代表教室编号
#             bid = 0
#             if c.credit == 2:
#                 tmp[0] = str(2)
#                 tmp[1] = str(Day[Arr2[i][k]])
#                 tmp[2] = str(Time[Arr2[i][k]])
#                 tmp[3] = str(bid)
#                 tmp[4] = str(shuf[Arr2[i][k]][Cls2[i][k] - 1] // 100)
#                 tmp[5] = str((shuf[Arr2[i][k]][Cls2[i][k] - 1] // 10) % 10)
#                 tmp[6] = str(shuf[Arr2[i][k]][Cls2[i][k] - 1] % 10)
#                 k += 1
#                 print('azzz', tmp)
#             elif c.credit == 3:
#                 tmp[0] = str(3)
#                 tmp[1] = str(Day[Arr3[i][v]])
#                 tmp[2] = str(Time[Arr3[i][v]])
#                 tmp[3] = str(bid)
#                 tmp[4] = str(shuf[Arr3[i][k]][Cls3[i][k] - 1] // 100)
#                 tmp[5] = str((shuf[Arr3[i][k]][Cls3[i][k] - 1] // 10) % 10)
#                 tmp[6] = str(shuf[Arr3[i][k]][Cls3[i][k] - 1] % 10)
#                 v += 1
#             elif c.credit == 4:
#                 tmp[0] = str(2)
#                 tmp[1] = str(Day[Arr2[i][k]])
#                 tmp[2] = str(Time[Arr2[i][k]])
#                 tmp[3] = str(bid)
#                 tmp[4] = str(shuf[Arr2[i][k]][Cls2[i][k] - 1] // 100)
#                 tmp[5] = str((shuf[Arr2[i][k]][Cls2[i][k] - 1] // 10) % 10)
#                 tmp[6] = str(shuf[Arr2[i][k]][Cls2[i][k] - 1] % 10)
#                 k += 1
#
#                 tmp[7] = str(2)
#                 tmp[8] = str(Day[Arr2[i][k]])
#                 tmp[9] = str(Time[Arr2[i][k]])
#                 tmp[10] = str(bid)
#                 tmp[11] = str(shuf[Arr2[i][k]][Cls2[i][k] - 1] // 100)
#                 tmp[12] = str((shuf[Arr2[i][k]][Cls2[i][k] - 1] // 10) % 10)
#                 tmp[13] = str(shuf[Arr2[i][k]][Cls2[i][k] - 1] % 10)
#                 k += 1
#             elif c.credit == 5:
#                 tmp[0] = str(2)
#                 tmp[1] = str(Day[Arr2[i][k]])
#                 tmp[2] = str(Time[Arr2[i][k]])
#                 tmp[3] = str(bid)
#                 tmp[4] = str(shuf[Arr2[i][k]][Cls2[i][k] - 1] // 100)
#                 tmp[5] = str((shuf[Arr2[i][k]][Cls2[i][k] - 1] // 10) % 10)
#                 tmp[6] = str(shuf[Arr2[i][k]][Cls2[i][k] - 1] % 10)
#                 k += 1
#
#                 tmp[7] = str(3)
#                 tmp[8] = str(Day[Arr3[i][v]])
#                 tmp[9] = str(Time[Arr3[i][v]])
#                 tmp[10] = str(bid)
#                 tmp[11] = str(shuf[Arr2[i][k]][Cls2[i][k] - 1] // 100)
#                 tmp[12] = str((shuf[Arr2[i][k]][Cls2[i][k] - 1] // 10) % 10)
#                 tmp[13] = str(shuf[Arr2[i][k]][Cls2[i][k] - 1] % 10)
#                 v += 1
#             Class2[i] += dic[c.credit][1]
#             Class3[i] += dic[c.credit][2]
#         print('rnm')
#         if tmp[8] != "0" and (int(tmp[1]) > int(tmp[8]) or int(tmp[1]) == int(tmp[8]) and int(tmp[2]) > int(tmp[9])):
#             tmp[0:7], tmp[7:14] = tmp[7:14], tmp[0:7]
#         c.time = ''.join(tmp)
#         print('tuiqian')
#
#     db = get_db()
#     db.session.commit()
#     Courses = TermCourse.query.all()
#     print('bnm')
#     a = []
#     Classrooms = Classroom.query.filter(Classroom.status == 0).all()
#     location = []
#     for c in Classrooms:
#         location.append(c.location)
#         print(c.location)
#     for c in Courses:
#         print('gdsg')
#         b = []
#         Teachers = Teacher.query.filter(Teacher.teacher_id == c.teacher_id).first()
#         # Classrooms = Classroom.query.filter(Classroom.id == c.time[4:7] and Classroom.status == 0).first()
#         b.append(c.course_id)
#         b.append(c.course_name)
#         b.append(Teachers.teacher_name)
#         b.append(decoder(c.time))
#         b.append(location[int(c.time[4:7])])
#         a.append(b)
#     flash(error)
#     return redirect(url_for('classarrange.department'))
#     # return render_template('department.html', Courses=a)
#     # return render_template('department.html', Courses=Courses)
#
#
# # @bp.route('/TeacherCourse', methods=['POST', 'GET'])
# # def TeacherCourse():
# #     if request.method == 'POST':
# #
# #         a = []
# #         Courses = TermCourse.filter(TermCourse.teacher_id == request.form['id']).all()
# #
# #     return render_template('department.html', Courses=a)
# @bp.route('/TeacherCourse', methods=['POST', 'GET'])
# @login_required
# def TeacherCourse():
#     a = []
#     period = ["08:00~09:35", "09:50~11:25", "11:30~12:15", "13:15~14:50",
#               "14:55~15:40", "15:55~17:30", "18:30~20:05", "20:10~20:55"]
#     for i in range(8):
#         tmp = [period[i]]
#         for j in range(5):
#             tmp.append(" ")
#         a.append(tmp)
#     b = [1, 2, 4, 6, 7]  # 221 212 21
#     teacher = Teacher.query.filter(Teacher.teacher_name == request.args.get('name')).first()
#     print(teacher)
#     if not teacher:
#         teacher = Teacher.query.filter(Teacher.teacher_id == current_user.uid).first()
#         applications = ModifyApplication.query.filter_by(teacher_id=teacher.teacher_id).all()
#
#     name = teacher.teacher_name
#     error = None
#     if teacher:
#         teacher = Teacher.query.filter(Teacher.teacher_name == request.args.get('name')).first()
#         print(str(teacher.teacher_id).zfill(5))
#         courses = TermCourse.query.filter(TermCourse.teacher_id == str(teacher.teacher_id).zfill(5)).all()
#         print(courses)
#         applications = ModifyApplication.query.filter_by(teacher_id=teacher.teacher_id).order_by(
#             ModifyApplication.id.desc()).all()
#         for c in courses:
#             for i in [0, 7]:
#                 if (c.time[i] == '0'):
#                     break
#                 else:
#                     a[b[int(c.time[i + 2]) - 1] - 1][int(c.time[i + 1])] = c.course_name
#                     if (c.time[i] == '3'):
#                         a[b[int(c.time[i + 2]) - 1]][int(c.time[i + 1])] = c.course_name
#                     # a[b[int(c.time[i + 1])]][int(c.time[i + 2])] = c.course_name
#                     # if(c.time[i+3]=='3'):
#                     #     a[b[int(c.time[i + 1])]+1][int(c.time[i + 2])] = c.course_name
#         print(applications)
#     return render_template('ClassArrange/teachermain.html', Courses=a, applications=applications)
#
#
# @bp.route('/submitapply', methods=['POST', 'GET'])
# @login_required
# def submitapply():
#     if request.method == 'POST':
#         error = None
#         # *********************************这里要用教师名！！！！*****************************************#
#         teacher_id = current_user.uid
#         # *********************************这里要用教师名！！！！*****************************************#
#
#         content = request.form['content']
#         # 0:未处理 1：处理完成 2：被拒绝
#         statecode = 0
#         if len(content) > 200:
#             error = "字数超过上限！"
#         elif content is None:
#             error = "未填写内容！"
#         else:
#             applcation = ModifyApplication(teacher_id=teacher_id, content=content, statecode=statecode)
#             db = get_db()
#             db.session.add(applcation)
#             db.session.commit()
#             error = "提交申请成功"
#         flash(error)
#     return redirect(url_for('classarrange.TeacherCourse'))
#
#
# @bp.route('/processapplication', methods=['POST', 'GET'])
# @login_required
# def processapplication():
#     if request.method == 'POST':
#         # *********************************这里要用教师名！！！！*****************************************#
#         id = request.form['id']
#         # *********************************这里要用教师名！！！！*****************************************#
#         # content = request.form['content']
#         statecode = request.form['statecode']
#         # *********************************这里要用管理员名！！！！*****************************************#
#         handler = current_user.uid
#         # *********************************这里要用管理员名！！！！*****************************************#
#
#         application = ModifyApplication.query.filter_by(id=id).first()
#         if application is not None:
#             application.statecode = statecode
#             application.handler = handler
#             db = get_db()
#             db.session.add(application)
#             db.session.commit()
#             error = "处理成功！"
#         else:
#             error = "处理失败！"
#         flash(error)
#     return redirect(url_for('classarrange.application'))
#
#
# @bp.route('/prints')
# @login_required
# def prints():
#     import pandas as pd
#     a = []
#     period = ["08:00~09:35", "09:50~11:25", "11:30~12:15", "13:15~14:50",
#               "14:55~15:40", "15:55~17:30", "18:30~20:05", "20:10~20:55"]
#     for i in range(8):
#         tmp = [period[i]]
#         for j in range(5):
#             tmp.append(" ")
#         a.append(tmp)
#     b = [1, 2, 4, 6, 7]  # 221 212 21
#
#     error = None
#     if not request.args.get('name'):
#         error = 'name is required'
#         flash(error)
#     else:
#         teacher = Teacher.query.filter(Teacher.teacher_name == request.args.get('name')).first()
#         courses = TermCourse.query.filter(TermCourse.teacher_id == str(teacher.teacher_id).zfill(5)).all()
#         for c in courses:
#             for i in [0, 7]:
#                 if (c.time[i] == '0'):
#                     break
#                 else:
#                     a[b[int(c.time[i + 2]) - 1] - 1][int(c.time[i + 1])] = c.course_name
#                     if (c.time[i] == '3'):
#                         a[b[int(c.time[i + 2]) - 1]][int(c.time[i + 1])] = c.course_name
#                     # a[b[int(c.time[i + 1])]][int(c.time[i + 2])] = c.course_name
#                     # if(c.time[i+3]=='3'):
#                     #     a[b[int(c.time[i + 1])]+1][int(c.time[i + 2])] = c.course_name
#         print(a)
#         df = pd.DataFrame(a, columns=["time", "周一", "周二", "周三", "周四", "周五"])
#         df.to_csv("hhh.csv", index=False)
#     return redirect(url_for('classarrange.teachermain'))
#
#
# @bp.route('/printtable', methods=['POST'])
# @login_required
# def printtable():
#     import pandas as pd
#     a = []
#     period = ["08:00~09:35", "09:50~11:25", "11:30~12:15", "13:15~14:50",
#               "14:55~15:40", "15:55~17:30", "18:30~20:05", "20:10~20:55"]
#     for i in range(8):
#         tmp = [period[i]]
#         for j in range(5):
#             tmp.append(" ")
#         a.append(tmp)
#     b = [1, 2, 4, 6, 7]  # 221 212 21
#     application = ModifyApplication.query.filter_by().order_by(ModifyApplication.id.desc()).all()
#     error = None
#     # if not g.name:
#     if not current_user.uid:
#         error = 'name is required'
#         flash(error)
#     else:
#         try:
#             teacher = Teacher.query.filter(Teacher.teacher_id == current_user.uid).first()
#             # teacher = Teacher.query.filter(Teacher.teacher_name == request.args.get('name')).first()
#             courses = TermCourse.query.filter(TermCourse.teacher_id == teacher.teacher_id).all()
#         except:
#             flash('fuck')
#             return redirect(url_for('classarrange.TeacherCourse'))
#         for c in courses:
#             for i in [0, 7]:
#                 if (c.time[i] == '0'):
#                     break
#                 else:
#                     a[b[int(c.time[i + 2]) - 1] - 1][int(c.time[i + 1])] = c.course_name
#                     if (c.time[i] == '3'):
#                         a[b[int(c.time[i + 2]) - 1]][int(c.time[i + 1])] = c.course_name
#                     # a[b[int(c.time[i + 1])]][int(c.time[i + 2])] = c.course_name
#                     # if(c.time[i+3]=='3'):
#                     #     a[b[int(c.time[i + 1])]+1][int(c.time[i + 2])] = c.course_name
#         print(a)
#         df = pd.DataFrame(a, columns=["time", "周一", "周二", "周三", "周四", "周五"])
#         # df.to_csv("ClassSchedule.csv", index=False)
#         df.to_csv(current_user.name + ".csv", index=False)
#         # df.to_csv(g.name + "csv", index=False)
#         flash("打印成功！")
#     return redirect(url_for('classarrange.TeacherCourse'))
#     # return render_template('teachermain.html', Courses=a,application=application);
