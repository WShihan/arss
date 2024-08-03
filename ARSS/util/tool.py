# -*- coding: utf-8 -*-
"""
    @File: tool.py
    @Author:Wang Shihan
    @Date:2024/7/25
    @Description:
"""
from datetime import datetime
from uuid import uuid4
from random import randint


def extract_attr(obj: object) -> dict:
    prop_dict = vars(obj)
    response_dict = {}
    for k, v in prop_dict.items():
        if k.startswith("_") or k.endswith("_"):
            continue
        if isinstance(v, datetime):
            prop_v = v.strftime('%Y-%m-%d %H:%M:%d')
        else:
            prop_v = v
        response_dict[k] = prop_v
    return response_dict


def short_uuid(num=8) -> str:
    """
    获取八位随机uid
    :return:
    """
    uid = str(uuid4().int)
    head = randint(0, 30)
    id = uid[head: head + num]
    return id.zfill(num)