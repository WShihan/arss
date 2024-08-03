# -*- coding: utf-8 -*-
"""
    @File: jwt.py
    @Author:Wang Shihan
    @Date:2024/8/2
    @Description:
"""
from flask_jwt_extended import JWTManager
from ARSS import app

jwt = JWTManager(app)




