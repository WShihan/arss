# -*- coding: utf-8 -*-
"""
    @File: user.py
    @Author:Wang Shihan
    @Date:2024/8/2
    @Description:
"""
from flask import request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
import base64
from ARSS import app
from ARSS.models import User
from ARSS.hooks import universal_api
from ARSS.store import Store


@app.route('/arss/api/user/login', methods=['POST'])
@universal_api
def user_login():
    args: dict = request.json
    password = args['password'].strip()
    encode_pass = base64.b64encode(password.encode('utf8')).decode('utf8')
    username = args['username']
    user = User.query.filter(User.username == username, User.password == encode_pass).first()
    if user:
        ak = create_access_token(identity=username)
        return {'access_token': f'Bearer {ak}',
                'username': username}

    else:
        raise ValueError('无用户，请检查用户名或密码！')


@app.route('/arss/api/user/create', methods=['POST'])
@universal_api
def user_create():
    args: dict = request.json
    encode_pass = base64.b64encode(args['password'].encode('utf8')).decode('utf8')
    username = args['username']
    admin = args.get('admin', False)
    user = User.query.filter(
        User.username == username,
        User.password == encode_pass
    ).first()
    if user:
        raise ValueError('用户名已存在！')
    else:
        user = User(
            username=username,
            password=encode_pass,
            admin=admin,
        )
        Store.save(user)
        ak = create_access_token(identity=username)
        return {'access_token': f'Bearer {ak}',
                'username': username}


@app.route('/arss/api/user/update', methods=['POST'])
@jwt_required()
@universal_api
def user_update():
    args: dict = request.json
    encode_pass = base64.b32encode(args['password'])
    username = args['username']
    user = User.query.filter(User.username == username, User.password == encode_pass).first()
    if user:
        raise ValueError('用户名已存在！')
    else:
        user = User(
            username=username,
            password=encode_pass,
        )
        Store.save(user)
        ak = create_access_token(identity=username)
        return {'access_token': f'Bearer {ak}'}


@app.route('/arss/api/user/all', methods=['POST', 'GET'])
@universal_api
@jwt_required()
def user_all():
    username = get_jwt_identity()
    user = User.query.filter(User.username == username).first()
    if user:
        if user.admin:
            users = User.query.all()
            return [{'username': u.username, 'admin': u.admin, } for u in users]
        else:
            raise ValueError('无权限')
    else:
        raise ValueError('无记录')


@app.route('/arss/api/user/refresh', methods=['POST', 'GET'])
@universal_api
@jwt_required()
def user_refresh():
    username = get_jwt_identity()
    user = User.query.filter(User.username == username).first()
    if user:
        ak = create_access_token(identity=username)
        return {'access_token': f'Bearer {ak}'}

    else:
        raise ValueError('无记录')
