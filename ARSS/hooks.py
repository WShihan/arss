# -*- coding: utf-8 -*-
"""
    @File: hooks.py
    @Author:Wang Shihan
    @Date:2024/7/25
    @Description:
"""
# from flask import g
# from flask_jwt_extended import get_jwt_identity, jwt_required
from ARSS import app
from ARSS.api.response import ApiResponse
# from ARSS.models import User
from functools import wraps


# @app.after_request
# def requests_after_hook(response):


def universal_api(func):
    """
    统一接口返回数据类型
    """

    def log_except(e: Exception):
        app.logger.error(str(e))
        return ApiResponse(str(e), code=400).failed

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            return ApiResponse(data=response).success
        except Exception as e:
            return log_except(e)

    return wrapper
