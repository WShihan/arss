# -*- coding: utf-8 -*-
"""
    @File: aggregater.py
    @Author:Wang Shihan
    @Date:2024/8/2
    @Description:
"""
from ARSS import app
from ARSS.models import Aggregater, Aggregates, Feed, Entry
from ARSS.store import Store
from ARSS.util.tool import short_uuid
import logging
from datetime import datetime


class AggregaterProcessor:
    @classmethod
    def refresh(cls, agger: Aggregater):
        with app.app_context():
            try:
                entries = []
                now = datetime.now()
                for feed in agger.feeds:
                    for entry in feed.entries:
                        if entry.agg_id is None:
                            entries.append(entry)

                if len(entries) == 0:
                    return
                agge = Aggregates(
                    title=f'{now.strftime("%y-%m-%d")}-{agger.title}',
                    publish=now,
                    guid=short_uuid(12),
                    userid=agger.userid,
                    aggregater=agger.id,
                )
                Store.save(agge)

                content = '[TOC]\n\n'
                for i in range(len(entries)):
                    entry = entries[i]
                    content += f'# {i + 1}.{entry.title}\n{entry.summary}\n[全文]({entry.link})\n'
                    entry.agg_id = agge.guid

                agge.content = content
                Store.update(agge)

            except Exception as e:
                logging.error(e)
