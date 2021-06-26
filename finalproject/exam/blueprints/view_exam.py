from flask import Blueprint
from sqlalchemy import desc

from database import db
from flask import render_template, request, flash, redirect, url_for
from datetime import datetime
from exam.models.answer import Anspa_prob_answer, Anspaper
import time

from models import Paper

view_exam_bp = Blueprint('view_exam', __name__)


@view_exam_bp.route('/')
def home():
    dt1 = time
    exams = Paper.query.order_by(desc(Paper.end_t)).all()
    return render_template('Exam/exam/view_exam.html', exams=exams, time=dt1)


# 0 表示考试未开始， 1 表示考试已结束， 2 表示考试可以开始， 3 表示考试已结束
@view_exam_bp.route('/information/<int:paper_id>')
def show_information(paper_id):
    exam = Paper.query.filter_by(paper_id=paper_id).first()
    length = len(exam.problems)
    dt1 = time.time()
    dt2 = time.mktime(exam.strt_t.timetuple())  # 开始时间
    dt3 = time.mktime(exam.end_t.timetuple())  # 结束时间
    anspapers = Anspaper.query.filter_by(paper_id=paper_id).order_by(desc(Anspaper.score_all)).all()
    if dt1>dt3:
        label = 1
        if anspapers(0).Ranknum == 0:
            prescore = -1  # 记录前一人的分数
            rank_count = 1
            for anspaper in anspapers:  # 计算平均分
                if anspaper.score_all != prescore:
                    rank = rank_count
                rank_count += 1
                anspaper.Ranknum = rank
                prescore = anspaper.score_all
            db.session.commit()
    elif dt1<dt2:
        label = 0
    elif exam.end:
        label = 3
    else:
        label = 2
    t = int(int(dt3-dt2)/60)
    # print(t)
    return render_template('Exam/exam/exam_info.html', exam=exam, label=label, length=length, t=t, anspapers=anspapers)
