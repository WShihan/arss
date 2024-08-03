# -*- coding: utf-8 -*-
"""
    @File: aggregater.py
    @Author:Wang Shihan
    @Date:2024/7/25
    @Description:
"""
from flask import request
from ARSS import app
from ARSS.store import Store
from ARSS.models import Aggregater, Aggregates, User
from ARSS.hooks import universal_api
from ARSS.util.tool import extract_attr
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from ARSS.processor.aggregater import AggregaterProcessor


@app.route('/arss/api/agger/create', methods=['POST'])
@jwt_required()
@universal_api
def aggregate_create():
    data: dict = request.json
    username = get_jwt_identity()
    user = User.query.filter(User.username == username).first()
    if not user:
        raise ValueError('无记录！')

    title = data['title']
    prompt = data.get('prompt')
    agg = Aggregater(
        title=title,
        userid=user.id,
        prompt=prompt
    )
    Store.save(agg)


@app.route('/arss/api/agger/all', methods=['GET'])
@jwt_required()
@universal_api
def aggregate_all():
    username = get_jwt_identity()
    user = User.query.filter(User.username == username).first()
    data = []
    if user:
        aggs = Aggregater.query.filter(Aggregater.userid == user.id).all()
        for agg in aggs:
            agg: Aggregater = agg
            data.append({
                'id': agg.id,
                'userid': agg.userid,
                'title': agg.title,
                'feeds': len(agg.feeds),
                'prompt': agg.prompt

            })
        return data
    else:
        raise ValueError('无记录')


@app.route('/arss/api/agger/one', methods=['POST'])
@universal_api
def aggregate_one():
    userid = request.args['userid']
    id = request.args['id']
    agg = Aggregater.query.filter(
        Aggregater.userid == userid,
        Aggregater.id == id).first()
    if agg:
        return extract_attr(agg)
    else:
        raise ValueError("无记录")


@app.route('/arss/api/agger/update', methods=['POST'])
@universal_api
def aggregate_update():
    id = request.args['id']
    userid = request.args['userid']
    data: dict = request.json
    agg = Aggregater.query.filter(
        Aggregater.userid == userid,
        Aggregater.id == id).first()
    if agg:
        for k, v in data.items():
            setattr(agg, k, v)
    else:
        raise ValueError("无记录")


@app.route('/arss/api/agger/delete', methods=['POST'])
@universal_api
def aggregate_delete():
    id = request.args['id']
    userid = request.args['userid']
    agg = Aggregater.query.filter(
        Aggregater.userid == userid,
        Aggregater.id == id).first()
    if agg:
        Store.delete(agg)
    else:
        raise ValueError("无记录")


@app.route('/arss/api/agger/refresh', methods=['GET'])
@universal_api
def aggregate_refresh():
    id = request.args['id']
    userid = request.args['userid']
    contents = {}

    agg = Aggregater.query.filter(
        Aggregater.userid == userid,
        Aggregater.id == id).first()
    if agg:
        for feed in agg.feeds:
            for entry in feed.entries:
                if entry.agg_id is None:
                    date = entry.publish.strftime('%Y-%m-%d')
                    if contents.get(date):
                        contents[date].append(entry)
                    else:
                        contents[date] = [entry]
        now = datetime.now()
        content = ''
        for k, v in contents.items():
            content += f'-----{k}-----\n'
            for entry in v:
                content += entry.content + '\n'
                entry.agg_id = agg.id

        agg_entry = Aggregates(
            title=f'{agg.title}-' + now.strftime('%Y-%m-%d'),
            userid=userid,
            content=content
        )
        agg.entries.append(agg_entry)
        Store.save(agg)

    else:
        raise ValueError("无记录")


@app.route('/arss/api/agger/refresh/<id>', methods=['GET', 'POST'])
@universal_api
def agg_refresh(id):
    agg = Aggregater.query.filter(Aggregater.id == id).first()
    if agg:
        AggregaterProcessor.refresh(agg)
    else:
        raise ValueError('无记录')



@app.route('/arss/view/<id>', methods=['GET', 'POST'])
def agg_view(id):
    agg = Aggregates.query.filter(Aggregater.id == id).first()
    if agg:
        return agg.content
    else:
        raise ValueError('无记录')
