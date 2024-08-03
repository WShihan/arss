# -*- coding: utf-8 -*-
"""
    @File: translater.py
    @Author:Wang Shihan
    @Date:2024/7/26
    @Description:
"""
from ARSS.util.llm import LLM
from ARSS import app


class Translater:
    def __init__(self, prompt='你是一个翻译助手，将下面这段文字翻译成中文。'):
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


if __name__ == '__main__':
    translate = Translater()
    res = translate.run('Build a GUI Calculator With PyQt and Python')
    print(res)
