# -*- coding: utf-8 -*-
"""
    @File: feed.py
    @Author:Wang Shihan
    @Date:2024/7/25
    @Description:
"""
from flask import request, make_response
from ARSS import app
from ARSS.models import Feed, Aggregater, User
from ARSS.hooks import universal_api
from ARSS.util.tool import extract_attr
from ARSS.processor.feed import FeedProcessor
from ARSS.store import Store
from flask_jwt_extended import jwt_required, get_jwt_identity


@app.route('/arss/api/feed/create', methods=['POST'])
@jwt_required()
@universal_api
def feed_create():
    args = request.json
    userid = args['userid']
    url = args['url']
    agg_id = args['agg_id']

    agg = Aggregater.query.filter(Aggregater.userid == userid, Aggregater.id == agg_id).first()
    exist_feed = Feed.query.filter(Feed.url == url).first()
    if exist_feed:
        raise ValueError('订阅源已经存在')
    if agg is None:
        raise ValueError('无聚合器记录')

    feed = FeedProcessor.find_feed(**args)
    if feed:
        agg.feeds.append(feed)
        Store.save(agg, feed)
    else:
        raise ValueError('解析feed错误，请检查url')


@app.route('/arss/api/feed/all', methods=['GET'])
@jwt_required()
@universal_api
def feed_all():
    user = User.query.filter(User.username == get_jwt_identity()).first()
    if not user:
        raise ValueError('无记录')
    return [extract_attr(a) for a in Feed.query.filter(Feed.userid == user.id).order_by(Feed.create_at.desc()).all()]


@app.route('/arss/api/feed/one', methods=['POST'])
@universal_api
def feed_one():
    userid = request.args['userid']
    id = request.args['id']
    agg = Feed.query.filter(
        Feed.userid == userid,
        Feed.id == id).first()
    if agg:
        return extract_attr(agg)
    else:
        raise ValueError("无记录")


@app.route('/arss/api/feed/update', methods=['POST'])
@universal_api
def feed_update():
    id = request.args['id']
    userid = request.args['userid']
    data: dict = request.json
    feed = Feed.query.filter(
        Feed.userid == userid,
        Feed.id == id).first()
    if feed:
        for k, v in data.items():
            setattr(feed, k, v)
        Store.update(feed)
    else:
        raise ValueError("无记录")


@app.route('/arss/api/feed/delete', methods=['POST'])
@universal_api
def feed_delete():
    id = request.args['id']
    userid = request.args['userid']
    feed = Feed.query.filter(
        Feed.userid == userid,
        Feed.id == id).first()
    if feed:
        Store.delete(*feed.entries)
        Store.delete(feed)
    else:
        raise ValueError("无记录")


