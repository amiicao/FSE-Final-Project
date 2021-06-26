from flask import Blueprint, render_template_string
from flask_sqlalchemy import SQLAlchemy

import pymysql

bp = Blueprint('exam', __name__, url_prefix='/exam', static_folder='static')

@bp.route('/')
def main():
    return 'exam blueprint ok'


from exam.commands import initdb, forge_problems
from exam.blueprints.problem import problem_bp
from exam.blueprints.manage_exam import manage_exam_bp
from exam.blueprints.view_exam import view_exam_bp
from exam.blueprints.take_exam import take_exam_bp
from exam.blueprints.teacher import teacher_bp

bp.register_blueprint(problem_bp, url_prefix='/problem')
bp.register_blueprint(manage_exam_bp, url_prefix='/manage_exam')
bp.register_blueprint(view_exam_bp, url_prefix='/view_exam')
bp.register_blueprint(take_exam_bp, url_prefix='/take_exam')
bp.register_blueprint(teacher_bp, url_prefix='/teacher_result')