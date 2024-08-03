# -*- coding: utf-8 -*-
"""
    @File: feed.py
    @Author:Wang Shihan
    @Date:2024/7/26
    @Description:
"""
import re
from ARSS.models import Feed
import feedparser
from datetime import datetime
from ARSS.processor.entry import EntryProcessor
from ARSS import app


class FeedProcessor:
    @staticmethod
    def parse(url):
        return feedparser.parse(url)

    @classmethod
    def find_feed(cls, **kwargs) -> Feed or None:
        url = kwargs['url']
        translate_title = kwargs.get('translate_title', False)
        scrap_content = kwargs.get('scrap_content', False)
        f = feedparser.parse(url)
        entries = f.entries
        rss = f.get('feed')
        if rss.get('title'):
            title = rss['title']
            author = rss.get('author', rss.title)
            logo = rss.get('logo')
            guid = rss.get('id', title)
            feed = Feed(
                userid=kwargs['userid'],
                agg_id=kwargs['agg_id'],
                guid=guid,
                title=title,
                author=author,
                logo=logo,
                url=url,
                lang=rss.get('language'),
                translate_title=translate_title,
                scrap_content=scrap_content
            )
            for e in entries:
                entry = EntryProcessor.parser_entry(e)
                feed.entries.append(entry)
            cls.feed_postprocess(feed)
            feed.latest_fresh_date = datetime.now()
            feed.latest_fresh_success = True
            return feed
        else:
            return None

    @classmethod
    def refresh_entries(cls, feed: Feed):
        try:
            with app.app_context():
                url = feed.url
                app.logger.info(f'开始刷新feed:{url}')
                exist_id = [e.guid for e in feed.entries]
                append_entries = []
                f = feedparser.parse(url)
                for e in f.entries:
                    # 规则阻止
                    if cls.check_by_rule(feed, e.title):
                        continue
                    # 是否已存在
                    if e.id not in exist_id:
                        entry = EntryProcessor.parser_entry(e)
                        append_entries.append(entry)

                if len(append_entries) == 0:
                    return

                if feed.translate_title:
                    EntryProcessor.translate_title(append_entries)

                if feed.scrap_content:
                    EntryProcessor.scrap_content(append_entries)

                EntryProcessor.summarize_content(append_entries)
                feed.entries += append_entries
                app.logger.info(f'更新数量{len(append_entries)}')
        except Exception as e:
            app.logger.info(f'刷新feed 错误：{e}')
        finally:
            app.logger.info(f'结束刷新feed:{url}')

    @classmethod
    def feed_postprocess(cls, feed: Feed):
        if feed.translate_title:
            EntryProcessor.translate_title(feed.entries)

        if feed.scrap_content:
            EntryProcessor.scrap_content(feed.entries)

        EntryProcessor.summarize_content(feed.entries)

    @classmethod
    def check_by_rule(cls, feed: Feed, text: str) -> bool:
        status = False
        for r in feed.rules:
            sear_res = re.search(f'{r.content}', text) if r.case_sensitive else re.search(f'{r.content}', text, re.IGNORECASE)
            if sear_res is not None:
                status = True

        return status
