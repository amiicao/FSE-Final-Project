from flask import Blueprint
from sqlalchemy import desc, text

from database import db
from flask import render_template, request, flash, redirect, url_for
from datetime import datetime
from exam.models.answer import Anspa_prob_answer, Anspaper
from models import Student, Paper, Course
import time
from flask_login import current_user

view_exam_bp = Blueprint('view_exam', __name__)


@view_exam_bp.route('/')
def home():
    dt1 = time
    courses = Student.query.filter_by(id=current_user.uid).first().courses
    sql = ""
    flag = 0
    for course in courses:
        if flag == 0:
            flag = 1
            sql += "to_class="+str(course.cid)
        else:
            sql +=" or to_class="+str(course.cid)
    exams = Paper.query.filter(text(sql)).all()
    return render_template('Exam/exam/view_exam.html', exams=exams, time=dt1)


# 0 表示考试未开始， 1 表示考试已结束， 2 表示考试可以开始， 3 表示考试已结束
@view_exam_bp.route('/information/<int:paper_id>')
def show_information(paper_id):
    exam = Paper.query.filter_by(paper_id=paper_id).first()

    courses = Student.query.filter_by(id=current_user.uid).first().courses
    sql = ""
    flag = 0
    for course in courses:
        if flag == 0:
            flag = 1
            sql += "to_class=" + str(course.cid)
        else:
            sql += " or to_class=" + str(course.cid)
    checkexam = Paper.query.filter(text(sql)).filter(paper_id == paper_id).first()
    if checkexam is None:
        return redirect(url_for('exam.view_exam.home'))

    length = len(exam.problems)
    dt1 = time.time()
    dt2 = time.mktime(exam.strt_t.timetuple())  # 开始时间
    dt3 = time.mktime(exam.end_t.timetuple())  # 结束时间
    anspapers = Anspaper.query.filter_by(paper_id=paper_id).order_by(desc(Anspaper.score_all)).all()
    anscheck = Anspaper.query.filter_by(paper_id=paper_id, student_id=current_user.uid).first()  # 检验该学生是否已经进入过考试界面
    if dt1>dt3:
        label = 1
        n = len(anspapers)
        if n != 0:
            if anspapers[0].Ranknum == 0:
                prescore = -2  # 记录前一人的分数
                rank_count = 1
                for anspaper in anspapers:  # 计算排名
                    if anspaper.score_all != prescore:
                        rank = rank_count
                    rank_count += 1
                    anspaper.Ranknum = rank
                    prescore = anspaper.score_all
                db.session.commit()
    elif dt1<dt2:
        label = 0
    elif anscheck is not None:  # 学生已经进入过考试界面
        label = 3
    else:
        label = 2
    t = int(int(dt3-dt2)/60)
    # print(t)
    return render_template('Exam/exam/exam_info.html', exam=exam, label=label, length=length, t=t, anspapers=anspapers)
