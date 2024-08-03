# -*- coding: utf-8 -*-
"""
    @File: models.py
    @Author:Wang Shihan
    @Date:2024/7/25
    @Description:
"""
from ARSS import db
from datetime import datetime


class Feed(db.Model):
    __tablename__ = 'Feed'
    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(50), nullable=False)
    # 所属用户
    userid = db.Column(db.Integer, db.ForeignKey('User.id'))
    agg_id = db.Column(db.Integer, db.ForeignKey('Aggregater.id'), nullable=False)
    # 标题
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    lang = db.Column(db.String(50))
    # logo地址
    logo = db.Column(db.String(255), nullable=True)
    # 作者
    author = db.Column(db.String(255), nullable=True)
    create_at = db.Column(db.DateTime, default=datetime.now(), index=True)
    # 最近刷新日期
    latest_fresh_date = db.Column(db.DateTime, index=True)
    # 最近刷新结果
    latest_fresh_success = db.Column(db.Boolean, index=True)
    # 最近刷新结果消息
    latest_fresh_msg = db.Column(db.String(255), index=True)
    translate_title = db.Column(db.Boolean, default=False)
    translate_content = db.Column(db.Boolean, default=False)
    scrap_content = db.Column(db.Boolean, default=False)
    # 归属内容
    entries = db.relationship("Entry")
    # 归属规则
    rules = db.relationship("Rule")


class Entry(db.Model):
    __tablename__ = 'Entry'
    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(255), nullable=False, unique=True)
    agg_id = db.Column(db.String(255))
    title = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(255), nullable=False)
    publish = db.Column(db.DateTime, index=True)
    author = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text)
    # token使用量
    usage = db.Column(db.Float, default=0)
    tags = db.Column(db.String(255))
    feed = db.Column(db.Integer, db.ForeignKey('Feed.id'))


class Aggregates(db.Model):
    __tablename__ = 'Aggregates'
    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(255), nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    publish = db.Column(db.DateTime, default=datetime.now(), index=True)
    # 所属用户
    userid = db.Column(db.Integer, db.ForeignKey('User.id'))
    aggregater = db.Column(db.Integer, db.ForeignKey('Aggregater.id'))


class Aggregater(db.Model):
    __tablename__ = 'Aggregater'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now(), index=True)
    # 最近刷新日期
    latest_fresh_date = db.Column(db.DateTime, index=True)
    # 最近刷新结果
    latest_fresh_success = db.Column(db.Boolean, index=True)
    # 最近刷新结果消息
    latest_fresh_msg = db.Column(db.String(255), index=True)
    prompt = db.Column(db.Text, nullable=True)
    # 所属用户
    userid = db.Column(db.Integer, db.ForeignKey('User.id'))
    # 归属aggregate
    entries = db.relationship("Aggregates")
    feeds = db.relationship("Feed")


class Rule(db.Model):
    __tablename__ = 'Rule'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    # 类型 阻止：0，保持：1
    type = db.Column(db.Integer, nullable=False, default=0)
    # 所属feed
    feed = db.Column(db.Integer, db.ForeignKey('Feed.id'))
    # 所属用户
    userid = db.Column(db.Integer, db.ForeignKey('User.id'))
    content = db.Column(db.Text, nullable=True)
    # 是否大小写敏感
    case_sensitive = db.Column(db.Boolean, default=True)


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    token = db.Column(db.String(255))
    expires = db.Column(db.DateTime, index=True)
    # 归属聚合器
    aggregaters = db.relationship("Aggregater")
    # 归属规则
    rules = db.relationship("Rule")
