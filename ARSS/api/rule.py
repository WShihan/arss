# -*- coding: utf-8 -*-
"""
    @File: rule.py
    @Author:Wang Shihan
    @Date:2024/8/1
    @Description:
"""
from ARSS.models import Rule, User
from ARSS import app
from flask import request
from ARSS.store import Store
from ARSS.hooks import universal_api
from ARSS.util.tool import extract_attr


@app.route('/arss/api/rule/create', methods=["POST"])
@universal_api
def rule_create():
    args: dict = request.json
    userid = args['userid']
    feed_id = args['feed_id']
    title = args.get('title')
    content = args.get('content')
    type = args.get('type', 0)
    case_sensitive = args.get('case_sensitive', True)

    user = User.query.filter(User.id == userid).first()
    if user:
        rule = Rule(
            title=title,
            type=type,
            feed=feed_id,
            userid=userid,
            content=content,
            case_sensitive=case_sensitive,
        )
        Store.save(rule)
    else:
        raise ValueError('无用户！')


@app.route('/arss/api/rule/update', methods=["GET"])
@universal_api
def rule_update():
    args: dict = request.args
    return User.query.all


@app.route('/arss/api/rule/all', methods=["GET"])
@universal_api
def rule_all():
    args: dict = request.args
    userid = args['userid']
    rules = Rule.query.filter(Rule.userid == userid).all()
    return [extract_attr(r) for r in rules]


@app.route('/arss/api/rule/one', methods=["GET"])
@universal_api
def rule_one():
    args: dict = request.args
    id = args['id']
    userid = args['userid']
    return Rule.query.filter(Rule.id == id, Rule.userid == userid).first()


@app.route('/arss/api/rule/delete', methods=["GET"])
@universal_api
def rule_delete():
    args: dict = request.args
    id = args['id']
    userid = args['userid']
    rule = Rule.query.filter(Rule.id == id, Rule.userid == userid).first()
    if rule:
        Store.delete(rule)
    else:
        raise ValueError('无记录')



