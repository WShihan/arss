# -*- coding: utf-8 -*-
"""
    @file: __init__.py
    @Author:Wang Shihan
    @Date:2023/9/19
    @Description: 入口文件
"""
from flask import Flask
from flask_cors import CORS
from ARSS.log import Logger
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask('ARSS')
# 设置配置文件
app.config.from_pyfile('settings.py')
# 允许跨域
CORS(app, supports_credentials=True)


# 设置日志
logger = Logger()
logger.init_app(app)
# 数据库配置
db = SQLAlchemy(app)
mg = Migrate(app, db)


from ARSS import view
from ARSS import models
from ARSS.scheduler import refresh_feed
from ARSS.api import *
from ARSS.jwt import *


