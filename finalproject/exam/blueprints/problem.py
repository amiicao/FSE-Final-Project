from flask import Blueprint
from database import db
from exam.forms.problem import ProblemForm
from exam.models.problem import Problem, Tag
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user

problem_bp = Blueprint('problem', __name__)


@problem_bp.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect('/')
    if current_user.status not in ['教师', '管理员']:
        return redirect(url_for('exam.view_exam.home'))

    problems = Problem.query.all()
    return render_template('Exam/problem/index.html', problems=problems)


@problem_bp.route('/render-problem-edit', methods=['POST'])
def render_edit_form():
    if not current_user.is_authenticated:
        return redirect('/')
    if current_user.status not in ['教师', '管理员']:
        return redirect(url_for('exam.view_exam.home'))

    problem_id = int(request.form.get('id'))
    form = ProblemForm()
    form.problem_id.data = problem_id

    if problem_id != 0:
        problem = Problem.query.filter_by(problem_id=str(problem_id)).first()

        form.type.data = str(problem.type)
        form.text.data = problem.text
        form.choice_A.data = problem.choice_A
        form.choice_B.data = problem.choice_B
        form.choice_C.data = problem.choice_C
        form.choice_D.data = problem.choice_D
        form.solution.data = problem.solution
        form.adder.data = str(problem.adder)
        form.tags.data = ' '.join([x.tag_name for x in problem.tags])
    else:
        form.adder.data = str(current_user.uid)

    return render_template('Exam/problem/problem_edit_form.html', form=form)


@problem_bp.route('/delete-problem/<int:problem_id>', methods=['POST'])
def delete_problem(problem_id):
    if not current_user.is_authenticated:
        return redirect('/')
    if current_user.status not in ['教师', '管理员']:
        return redirect(url_for('exam.view_exam.home'))

    problem = Problem.query.filter_by(problem_id=problem_id).first()
    if problem is not None:
        for tag in problem.tags:
            problem.tags.remove(tag)
            if not tag.problems:
                db.session.delete(tag)
        db.session.delete(problem)
        db.session.commit()
    flash('删除题目成功。')
    return redirect(url_for('exam.problem.home'))


@problem_bp.route('/edit-problem', methods=['POST'])
def edit_problem():
    if not current_user.is_authenticated:
        return redirect('/')
    if current_user.status not in ['教师', '管理员']:
        return redirect(url_for('exam.view_exam.home'))

    form = ProblemForm()
    problem_id = form.problem_id.data
    print(form.adder.data)
    form.validate()



    if form.validate_on_submit():

        problem = Problem()
        if problem_id != 0:
            problem = Problem.query.filter_by(problem_id=problem_id).first()

        problem.type = form.type.data
        problem.text = form.text.data
        problem.choice_A = form.choice_A.data
        problem.choice_B = form.choice_B.data
        problem.choice_C = form.choice_C.data
        problem.choice_D = form.choice_D.data
        problem.solution = form.solution.data
        problem.adder = int(form.adder.data)

        if problem_id == 0:
            db.session.add(problem)

        new_tag_names = set(form.tags.data.split())
        for tag in problem.tags:
            if tag.tag_name not in new_tag_names:
                problem.tags.remove(tag)
                if not tag.problems:
                    db.session.delete(tag)
        for tag_name in new_tag_names:
            tag = Tag.query.filter_by(tag_name=tag_name).first()
            if tag is None:
                tag = Tag(tag_name=tag_name)
            if tag not in problem.tags:
                problem.tags.append(tag)

        db.session.commit()
        flash('题目更新成功。')
        return 'OK'

    for error in form.adder.errors:
        print(error)

    return render_template('Exam/problem/problem_edit_form.html', form=form)