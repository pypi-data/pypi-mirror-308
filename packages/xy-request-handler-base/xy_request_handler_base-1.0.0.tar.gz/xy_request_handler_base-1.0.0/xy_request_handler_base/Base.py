# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Base"
"""
  * @File    :   Base.py
  * @Time    :   2023/04/29 19:32:31
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   请求基类，处理django数据库阻塞问题
"""

from tornado.web import RequestHandler
from .IBase import IBase
from django.db import connection


class Base(RequestHandler, IBase):
    def prepare(self, *args, **kwargs):
        self.close_old_connections()
        connection.close()
        super().prepare(*args, **kwargs)

    def finish(self, *args, **kwargs):
        self.close_old_connections()
        connection.close()
        return super().finish(*args, **kwargs)
