import os

from flask_login import LoginManager

import configs
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database import db
from models import User
import logging

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    app.config.from_object(configs)
    app.config['UPLOAD_FOLDER'] = 'uploads'
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'login.login'  # 这个是我们没有登录的时候重定向到的地方
    login_manager.init_app(app)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_pyfile(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # @app.route('/')
    # def hello():
    #     return 'Hello, World!'

    import messagearrange
    app.register_blueprint(messagearrange.bp)
    import classarrange
    app.register_blueprint(classarrange.bp)
    import login
    app.register_blueprint(login.bp)
    import selectcourse
    app.register_blueprint(selectcourse.bp)
    import exam
    app.register_blueprint(exam.bp)
    import resourceandscore
    app.register_blueprint(resourceandscore.bp)

    app.debug = True
    handler = logging.FileHandler('flask.log')
    logging_format = logging.Formatter(  # 设置日志格式
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    # import eduresource
    # app.register_blueprint(eduresource.bp)
    # import class_teacher
    # app.register_blueprint(class_teacher.bp)

    # import classroom
    # app.register_blueprint(classroom.bp)
    @login_manager.user_loader
    def load_user(id):
        app.logger.info("Info message")
        app.logger.warning("Warning msg")
        app.logger.error("Error msg!!!")

        if id:
            try:
                return User.query.get(int(id))
            except:
                pass

    return app



