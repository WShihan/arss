# -*- coding: utf-8 -*-
"""
    @File: rss.py
    @Author:Wang Shihan
    @Date:2024/8/2
    @Description:
"""
from flask import  make_response
from feedgen.feed import FeedGenerator
from datetime import timezone, timedelta
from ARSS.models import Feed, Aggregater
from ARSS import app


@app.route('/arss/rss/feed/<id>', methods=['GET', 'POST'])
def feed_rss(id):
    feed = Feed.query.filter(Feed.id == id).first()
    if not feed:
        return '无记录'
    domain = 'https:wsh233.cn'
    tz_utc_8 = timezone(timedelta(hours=8))  # 创建时区UTC+8:00
    # 创建一个Feed对象
    fg = FeedGenerator()
    fg.id('https://www.wsh233.cn/')
    fg.author({'name': 'arss', 'email': '3443327820@qq.com'})
    fg.title('arss')
    fg.language('zh-CN')
    fg.description('arss-一个rss聚合器')
    fg.link(href=f"https://{domain}")
    fg.logo(f"https://{domain}/static/Favicon.ico")
    for entry in feed.entries:
        fe = fg.add_entry()
        fe.title(entry.title)
        fe.link(href=entry.link)
        fe.summary(entry.summary, type='html')
        fe.guid(entry.link, permalink=True)
        fe.author(name='wsh', email='3443327820@qq.com')
        fe.pubDate(entry.publish.replace(tzinfo=tz_utc_8))
        fe.pubdate(entry.publish.replace(tzinfo=tz_utc_8))
    response = make_response(fg.atom_str(pretty=True))
    response.headers.set('Content-Type', 'application/xml; charset=utf-8')
    return response


@app.route('/arss/rss/agg/<id>', methods=['GET', 'POST'])
def agg_rss(id):
    agg = Aggregater.query.filter(Aggregater.id == id).first()
    if not agg:
        return '无记录'
    domain = 'https:wsh233.cn'
    tz_utc_8 = timezone(timedelta(hours=8))  # 创建时区UTC+8:00
    # 创建一个Feed对象
    fg = FeedGenerator()
    fg.id('https://www.wsh233.cn/')
    fg.author({'name': 'arss', 'email': '3443327820@qq.com'})
    fg.title(agg.title)
    fg.language('zh-CN')
    fg.description('arss-一个rss聚合器')
    fg.link(href=f"https://{domain}")
    fg.logo(f"https://{domain}/static/Favicon.ico")
    for entry in agg.entries:
        fe = fg.add_entry()
        link = f'{domain}/arss/view/{entry.id}'
        fe.title(entry.title)
        fe.link(href=link)
        fe.summary(entry.content, type='html')
        fe.guid(link, permalink=True)
        fe.author(name='wsh', email='3443327820@qq.com')
        fe.pubDate(entry.publish.replace(tzinfo=tz_utc_8))
        fe.pubdate(entry.publish.replace(tzinfo=tz_utc_8))
    response = make_response(fg.atom_str(pretty=True))
    response.headers.set('Content-Type', 'application/xml; charset=utf-8')
    return response