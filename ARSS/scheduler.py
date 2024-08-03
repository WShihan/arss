# -*- coding: utf-8 -*-
"""
    @File: scheduler.py
    @Author:Wang Shihan
    @Date:2024/8/1
    @Description:
"""
from flask_apscheduler import APScheduler
from ARSS import app
from ARSS.models import Aggregater
from ARSS.processor.feed import FeedProcessor
from ARSS.processor.aggregater import AggregaterProcessor
from ARSS.processor.worker import Worker
from ARSS.store import Store


# 定时器
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


@scheduler.task('cron', id='f', hour=13, minute=18)
def refresh_feed():
    with app.app_context():
        aggs: list = Aggregater.query.all()
        current_agg = aggs.pop()
        feeds = current_agg.feeds
        max_workers = 5
        for i in range(0, len(feeds), max_workers):
            exe_feeds = feeds[max_workers*i:max_workers*i + max_workers]
            worker = Worker(max_workers)
            tasks = [worker.submit_task(FeedProcessor.refresh_entries, f)
                     for f in exe_feeds]
            worker.wait_for_completion(tasks)
            Store.update(*exe_feeds)


@scheduler.task('cron', id='refresh_aggregate', hour=15, minute=10)
def refresh_aggregate():
    with app.app_context():
        aggs: list = Aggregater.query.all()
        max_workers = 5
        for i in range(0, len(aggs), max_workers):
            exe_aggs = aggs[max_workers*i:max_workers*i + max_workers]
            worker = Worker(max_workers)
            tasks = [worker.submit_task(AggregaterProcessor.refresh, f)
                     for f in exe_aggs]
            worker.wait_for_completion(tasks)
            Store.update(exe_aggs)
