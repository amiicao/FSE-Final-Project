from app import app
from flask import render_template


@app.route('/')  # 首页(侧边栏)
def student_analysis():
    return render_template('sidebar_S.html')


@app.route('/student_HW')   # 作业提交_学生
def student_HW():
    return render_template('student_HW.html')


@app.route('/student_marks')   # 成绩查询_学生
def score_analysisS():
    return render_template('student_marks.html')


@app.route('/student_analysis')   # 成绩分析_学生
def student_analysis():
    return render_template('student_analysis.html')


@app.route('/teacher_resource')   # 资源分享_教师
def resource_management():
    return render_template('teacher_resource.html')


@app.route('/teacher_HW')   # 作业布置_教师
def teacher_HW():
    return teacher_HW('teacher_HW.html')


@app.route('/teacher_marks')   # 成绩录入_教师
def teacher_marks():
    return render_template('teacher_marks.html')


@app.route('/score_analysisT')   # 成绩分析_教师
def score_analysisT():
    return render_template('teacher_analysis.html')


@app.route('/score_request')   # 成绩修改_教师/管理员
def score_request():
    return render_template('score_request.html')