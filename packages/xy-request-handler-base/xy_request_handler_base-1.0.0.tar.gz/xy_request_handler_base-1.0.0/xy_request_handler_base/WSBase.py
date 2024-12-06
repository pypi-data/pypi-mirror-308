# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "WSBase"
"""
  * @File    :   WSBase.py
  * @Time    :   2023/04/29 22:48:31
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
"""

from tornado.websocket import WebSocketHandler
from .IBase import IBase
from django.db import connection


class WSBase(WebSocketHandler, IBase):
    def prepare(self, *args, **kwargs):
        self.close_old_connections()
        connection.close()
        super().prepare(*args, **kwargs)

    def finish(self, *args, **kwargs):
        self.close_old_connections()
        connection.close()
        return super().finish(*args, **kwargs)
