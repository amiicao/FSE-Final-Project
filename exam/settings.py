import os
import sys


SQLALCHEMY_COMMIT_ON_TEARDOWN = False
SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
SQLALCHEMY_TRACK_MODIFICATIONS = True

SQLALCHEMY_DATABASE_URI = 'mysql://fse_g7:FSE_group7@rm-2zeb626gl3ajx1372ho.mysql.rds.aliyuncs.com:3306/exam'
