# -*- coding: utf-8 -*-
"""
    @file: viewe.py
    @Author:Wang Shihan
    @Date:2023/9/19
    @Description: 路由
"""
from ARSS import app


@app.route('/')
def index():
    return "Hello, world!"
