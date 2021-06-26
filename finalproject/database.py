# 设置函数
from flask_sqlalchemy import SQLAlchemy
from flask import current_app, g
import configs
db = SQLAlchemy()

def get_db():
    if 'db' not in g or g.db != db:
        current_app.config.from_object(configs)
        db.init_app(current_app)
        g.db = db
    return g.db

