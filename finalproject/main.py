import os
import configs
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    app.config.from_object(configs)
    app.config['UPLOAD_FOLDER'] = 'uploads'
    db.init_app(app)
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_pyfile(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    import messagearrange
    app.register_blueprint(messagearrange.bp)
    import classarrange
    app.register_blueprint(classarrange.bp)

    # import eduresource
    # app.register_blueprint(eduresource.bp)
    # import class_teacher
    # app.register_blueprint(class_teacher.bp)

    # import classroom
    # app.register_blueprint(classroom.bp)

    return app
