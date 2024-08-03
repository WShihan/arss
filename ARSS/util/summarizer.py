# -*- coding: utf-8 -*-
"""
    @File: summarizer.py
    @Author:Wang Shihan
    @Date:2024/7/27
    @Description:
"""
from ARSS.util.llm import LLM
from ARSS import app


class Summarizer:
    def __init__(self, prompt='你作为一个文字处理助手，需要我用中文总结我发送给你的文字，尽量简洁一点。'):
        self.engine = LLM(
            api='https://api.deepseek.com/chat/completions',
            model='deepseek-chat',
            key='',
            prompt=prompt
        )
        self.prompt = prompt
        self.engine.set_config(prompt=self.prompt)

    def run(self, msg: str) -> tuple:
        resp = self.engine.run(msg)
        if len(resp['choices']) > 0:
            return resp['choices'][0]['message']['content'], resp['usage']['total_tokens']
        else:
            app.logger.error(f'翻译请求错误,请查看日志:{resp}')
            return ()

    def handle_result(self, data):
        pass


if __name__ == '__main__':
    s = Summarizer()
    msg = ''''''
    print(s.run(msg))
