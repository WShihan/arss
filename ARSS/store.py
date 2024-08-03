# -*- coding: utf-8 -*-
"""
    @File: store.py
    @Author:Wang Shihan
    @Date:2024/7/26
    @Description:
"""
from ARSS import db, app


class Store:
    @classmethod
    def save(cls, *args):
        try:
            for obj in args:
                if cls.check(obj):
                    db.session.add(obj)
            db.session.commit()
        except Exception as e:
            app.logger.error(e)

    @classmethod
    def update(cls, *args):
        cls.save(*args)

    @classmethod
    def delete(cls, *args):
        try:
            for obj in args:
                if cls.check(obj):
                    db.session.delete(obj)
            db.session.commit()
        except Exception as e:
            app.logger.error(e)

    @classmethod
    def check(cls, obj):
        return isinstance(obj, db.Model)


