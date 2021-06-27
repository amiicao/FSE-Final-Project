"""学生参加考试的相关视图函数"""
from flask import Blueprint
from flask import render_template, request, url_for, redirect, flash
from sqlalchemy import desc, text
from database import db
from exam.forms.answer import PaperForm, AnswerForm
from exam.models.problem import Problem
from exam.models.answer import Anspa_prob_answer, Anspaper
import time
from models import Paper, Student
from flask_login import current_user
take_exam_bp = Blueprint('take_exam', __name__)


@take_exam_bp.route('/', methods=['GET', 'POST'])
def home():
    if not current_user.is_authenticated:
        return redirect('/')
    if current_user.status in ['教师', '管理员']:  # 老师和管理员跳转责任试卷列表界面
        return redirect(url_for('exam.teacher.home'))
    return redirect(url_for('exam.view_exam.home'))


@take_exam_bp.route('/<int:exam_id>', methods=['GET', 'POST'])
def take_exam(exam_id):
    if not current_user.is_authenticated:
        return redirect('/')
    if current_user.status in ['教师', '管理员']:  # 老师和管理员跳转责任试卷列表界面
        return redirect(url_for('exam.teacher.home'))

    # 验证该学生是否有资格参加该考试
    courses = Student.query.filter_by(id=current_user.uid).first().courses
    sql = ""
    flag = 0
    for course in courses:
        if flag == 0:
            flag = 1
            sql += "to_class=" + str(course.cid)
        else:
            sql += " or to_class=" + str(course.cid)
    checkexam = Paper.query.filter(text(sql)).filter(Paper.paper_id == exam_id).first()
    if checkexam is None:
        return redirect(url_for('exam.view_exam.home'))

    # 验证学生是否第一次进入考试页面
    anscheck = Anspaper.query.filter_by(paper_id=exam_id, student_id=current_user.uid).first()
    if anscheck is None:   # 学生第一次进入考试页面，立即生成答卷，避免学生退出后再次进入
        answerpaper = Anspaper(paper_id=exam_id, student_id=current_user.uid, score_all=0)
        db.session.add(answerpaper)
        db.session.commit()
    else:  # 学生已有答卷存在,返回查看试卷详情界面
        flash('您已经结束该考试！')
        return redirect(url_for('exam.view_exam.show_information', paper_id=exam_id))

    problems = Paper.query.filter_by(paper_id=exam_id).first().problems
    paper = Paper.query.filter_by(paper_id=exam_id).first()

    length = len(problems)
    dt3 = time.mktime(paper.end_t.timetuple())
    dt1 = time.time()
    t = int(dt3-dt1)
    if dt1 > dt3:
        return redirect(url_for('exam.take_exam.show_exam', exam_id=exam_id))
    # print(t)

    if request.method == 'POST':
        answerpaper = Anspaper.query.filter_by(paper_id=exam_id, student_id=current_user.uid).first()
        fullscore = 0
        for problem in problems:
            answer = ""
            score = 0
            if problem.type != 2:
                answer = request.form.get(str(problem.problem_id))
                if answer == problem.solution:
                    score = 1
                    fullscore += 1
                # print(answer)
            else:
                answers = request.form.getlist(str(problem.problem_id))
                for ans in answers:
                    answer += ans
                if answer == problem.solution:
                    score = 1
                    fullscore += 1
            a = Anspa_prob_answer(problem_id=problem.problem_id, answer=answer, anspaper_id=answerpaper.anspaper_id, score=score)
            db.session.add(a)
            answerpaper.Answers.append(a)
            answerpaper.score_all = fullscore
        # db.session.add(answerpaper)
        db.session.commit()
        paper.end = True  # 这个变量毫无意义
        db.session.commit()
        flash('提交成功.')
        return redirect(url_for('exam.view_exam.home'))
    return render_template('Exam/exam/take_exam.html', exam=paper, problems=problems, exam_id=exam_id, length=length, t=t)


@take_exam_bp.route('/show_exam/<int:exam_id>')
def show_exam(exam_id):
    paper = Paper.query.filter_by(paper_id=exam_id).first()
    problems = Paper.query.filter_by(paper_id=exam_id).first().problems
    answerpaper = Anspaper.query.filter_by(paper_id=paper.paper_id, student_id=current_user.uid).first()
    # print(type(answerpaper.Answers))
    # for problem in problems:
    #     answer = answerpaper.Answers.filter_by(problem_id=problem.problem_id).first().answer
    #     right = problem.solution
        # if answer==right:

    return render_template('Exam/exam/show_list.html', problems=problems, exam=paper, answerpaper=answerpaper)

