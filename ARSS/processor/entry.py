# -*- coding: utf-8 -*-
"""
    @File: entry.py
    @Author:Wang Shihan
    @Date:2024/7/26
    @Description:
"""
from ARSS import app
from ARSS.util.translater import Translater
from ARSS.models import Entry
from ARSS.processor.worker import Worker
from ARSS.util.scrapper import Scrapper
from ARSS.util.summarizer import Summarizer
from datetime import datetime


class EntryProcessor:
    @classmethod
    def translate_title(cls, entries: list):
        try:
            translater = Translater()
            worker = Worker(10)

            def func(entry: Entry):
                title = entry.title
                res = translater.run(title)
                if len(res) >= 2:
                    t_title = res[0]
                    entry.title = f'{t_title}｜{title}'
                    usage = entry.usage if entry.usage else 0
                    usage += res[1]
                    entry.usage = usage
                    # app.logger.info(f'翻译entry 标题：{title}｜ {t_title}')

            futures = [worker.submit_task(func, e) for e in entries]
            worker.wait_for_completion(futures)
        except Exception as e:
            app.logger.error(f'翻译标题错误:{str(e)}')

    @classmethod
    def scrap_content(cls, entries: list):
        try:
            worker = Worker(10)

            def func(entry: Entry):
                url = getattr(entry, 'link')
                content = Scrapper.scrap_content(url)
                if content:
                    entry.content = content
                    # app.logger.info(f'爬取正文：{url}')

            futures = [worker.submit_task(func, e) for e in entries]
            worker.wait_for_completion(futures)

        except Exception as e:
            app.logger.error(f'爬取正文错误:{str(e)}')

    @classmethod
    def summarize_content(cls, entries: list):
        try:
            worker = Worker(10)
            summarizer = Summarizer(prompt='你作为一个文字处理助手，需要我用中文总结我发送给你的文字，尽量简洁一点。')

            def func(entry: Entry):
                res = summarizer.run(entry.content)
                if len(res) >= 2:
                    summary = res[0]
                    entry.summary = summary
                    usage = entry.usage if entry.usage else 0
                    usage += res[1]
                    entry.usage = usage
                    # app.logger.info(f'总结正文：{summary}')

            futures = [worker.submit_task(func, e) for e in entries]
            worker.wait_for_completion(futures)

        except Exception as e:
            app.logger.error(f'总结内容错误:{str(e)}')

    @classmethod
    def parser_entry(cls, e):
        publish = e.get('published')
        if not publish:
            publish = e.get('pubDate')

        if publish:
            publish = datetime.strptime(publish, '%a, %d %b %Y %H:%M:%S %z')
        else:
            publish = datetime.now()
        return Entry(
            guid=e['id'],
            link=e['link'],
            title=e['title'],
            author=e.get('author', ''),
            publish=publish,
            content=e.get('summary', '')
        )
