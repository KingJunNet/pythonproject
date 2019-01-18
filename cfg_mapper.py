# -*- coding: utf-8 -*-
# from core import singleton
from core.db_config import SqlDBConfig

def singleton(cls):
    instance = cls()
    instance.__call__ = lambda: instance
    return instance

@singleton
class OriShareResourceDBConfig(SqlDBConfig):
    def __init__(self):
        SqlDBConfig.__init__(self)

@singleton
class UserDBConfig(SqlDBConfig):
    def __init__(self):
        SqlDBConfig.__init__(self)