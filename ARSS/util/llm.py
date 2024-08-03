# -*- coding: utf-8 -*-
"""
    @File: llm.py
    @Author:Wang Shihan
    @Date:2024/7/26
    @Description:
"""
from requests import Session


class LLM:
    def __init__(self, **kwargs):
        """
        openai-like llm client
        params:
        key: str >> any
        api: str >> any, default openai's api
        model:str >> any, default chatgpt-3.5-turbo
        prompt:str >> any, default None
        """
        key = kwargs.get('key')
        if not key:
            raise ValueError('必须设置密钥')

        self.api = kwargs.get('api', 'https://openai.api2d.net/v1/chat/completions')
        self.model = kwargs.get('model', 'gpt-3.5-turbo')
        self.__headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {key}',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
        }
        self.prompt = kwargs.get('prompt')
        self.session = Session()

    def set_config(self, **kwargs):
        prompt = kwargs.get('prompt')
        api = kwargs.get('api')
        model = kwargs.get('model')
        if prompt:
            self.prompt = prompt
        if api:
            self.api = api
        if model:
            self.api = api

    def run(self, msg: str) -> dict:
        """
        :param msg:str >> any
        :return:
        """
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": msg}]
        }
        if self.prompt is not None:
            payload['messages'].insert(0, dict({'role': 'system', 'content': self.prompt}))

        res = self.session.post(self.api, headers=self.__headers, json=payload)
        if res.status_code == 200:
            return res.json()
        else:
            raise ValueError('网络请求错误！')

    def __repr__(self):
        return f'LLM client\n api: {self.api}\n model: {self.model}\n role: {self.prompt}'
