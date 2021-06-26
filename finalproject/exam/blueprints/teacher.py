from flask import Blueprint
from flask import render_template, request, flash, redirect, url_for
from datetime import datetime
import time

from sqlalchemy import desc

from database import db
from exam.models.answer import ProbAnalysis, Anspaper
from models import Paper
from flask_login import current_user

teacher_bp = Blueprint('teacher', __name__)


@teacher_bp.route('/', methods=['GET', 'POST'])
def home():
    if not current_user.is_authenticated:
        return redirect('/')
    if current_user.status not in ['教师', '管理员']:
        return redirect(url_for('exam.view_exam.home'))
    dt1 = time
    if current_user.status == '教师':
        exams = Paper.query.filter_by(teacher_id=current_user.uid).order_by(desc(Paper.end_t)).all()
    else:
        exams = Paper.query.order_by(desc(Paper.end_t)).all()
    return render_template('Exam/teacher/view_exam.html', exams=exams, time=dt1)


@teacher_bp.route('/information/<int:paper_id>')
def show_information(paper_id):
    if not current_user.is_authenticated:
        return redirect('/')
    if current_user.status not in ['教师', '管理员']:
        return redirect(url_for('exam.view_exam.home'))
    exam = Paper.query.filter_by(paper_id=paper_id).first()
    if current_user.status == '教师' and exam.teacher_id != current_user.uid:  # 该试卷并非该老师发布的
        return redirect(url_for('exam.teacher.home'))
    dt1 = time.time()
    dt2 = time.mktime(exam.strt_t.timetuple())  # 开始时间
    dt3 = time.mktime(exam.end_t.timetuple())  # 结束时间
    length = len(exam.problems)
    anspapers = Anspaper.query.filter_by(paper_id=paper_id).order_by(desc(Anspaper.score_all)).all()
    if dt1<dt2:
        label = 0
    elif dt1>dt3:
        label = 2
        if anspapers.first().Ranknum == 0:
            prescore = -1  # 记录前一人的分数
            rank_count = 1
            for anspaper in anspapers:  # 计算平均分
                if anspaper.score_all != prescore:
                    rank = rank_count
                rank_count += 1
                anspaper.Ranknum = rank
                prescore = anspaper.score_all
            db.session.commit()
    else:
        label = 1
    t = int(int(dt3 - dt2) / 60)
    return render_template('Exam/teacher/exam_info.html', exam=exam, label=label, length=length, t=t, anspapers=anspapers)


@teacher_bp.route('/show_exam/<int:paper_id>', methods=['GET', 'POST'])
def show_exam(paper_id):
    if not current_user.is_authenticated:
        return redirect('/')
    if current_user.status not in ['教师', '管理员']:
        return redirect(url_for('exam.view_exam.home'))
    exam = Paper.query.filter_by(paper_id=paper_id).first()
    if current_user.status == '教师' and exam.teacher_id != current_user.uid:  # 该试卷并非该老师发布的
        return redirect(url_for('exam.teacher.home'))
    problems = exam.problems
    if not exam.anlsflag:  # 每道题的解答结果还未分析
        answerpapers = Anspaper.query.filter_by(paper_id=paper_id).all()
        totalnum = Anspaper.query.filter_by(paper_id=paper_id).count()
        totalscore = 0
        for answerpaper in answerpapers:  # 计算平均分
            totalscore += answerpaper.score_all
        if totalnum == 0:
            exam.score = 0
        else:
            exam.score = totalscore / totalnum
        for problem in problems:  # 计算每道题的解答结果
            totalscore = 0
            null_count = 0
            t_count = 0
            f_count = 0
            a_count = 0
            b_count = 0
            c_count = 0
            d_count = 0
            if problem.type == 0:
                for answerpaper in answerpapers:
                    answer = answerpaper.Answers.filter_by(problem_id=problem.problem_id).first().answer
                    totalscore += answerpaper.Answers.filter_by(problem_id = problem.problem_id).first().score
                    if answer == "T":
                        t_count += 1
                    elif answer == "F":
                        f_count += 1
                    else:
                        null_count += 1
            elif problem.type == 1:
                for answerpaper in answerpapers:
                    answer = answerpaper.Answers.filter_by(problem_id = problem.problem_id).first().answer
                    totalscore += answerpaper.Answers.filter_by(problem_id=problem.problem_id).first().score
                    if answer == "A":
                        a_count += 1
                    elif answer == "B":
                        b_count += 1
                    elif answer == "C":
                        c_count += 1
                    elif answer == "D":
                        d_count += 1
                    else:
                        null_count += 1
            else:
                for answerpaper in answerpapers:
                    answer = answerpaper.Answers.filter_by(problem_id = problem.problem_id).first().answer
                    totalscore += answerpaper.Answers.filter_by(problem_id=problem.problem_id).first().score
                    if answer.find('A'):
                        a_count += 1
                    if answer.find('B'):
                        b_count += 1
                    if answer.find('C'):
                        c_count += 1
                    if answer.find('D'):
                        d_count += 1
                    if len(answer) == 0:
                        null_count += 1
            if totalnum == 0:
                accuracy = 0
            else:
                accuracy = totalscore / totalnum
            analysis = ProbAnalysis(exam_id=exam.paper_id, problem_id=problem.problem_id, A_count=a_count,
                                    B_count=b_count, C_count=c_count, D_count=d_count, T_count=t_count, F_count=f_count,
                                    NULL_count=null_count, accuracy=accuracy)
            db.session.add(analysis)
            db.session.commit()
        exam.anlsflag = True
        db.session.commit()
    exam = Paper.query.filter_by(paper_id=paper_id).first()
    return render_template('Exam/teacher/show_exam.html', exam=exam)








