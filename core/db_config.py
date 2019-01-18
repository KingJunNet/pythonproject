# -*- coding: utf-8 -*-
from core import singleton

class SqlDBConfig:
    def __init__(self):
        self.host = ''
        self.db_name = ''
        self.user = ''
        self.pwd = ''

    def init(self,host,db_name,user,pwd):
        self.host = host
        self.db_name = db_name
        self.user = user
        self.pwd = pwd

    def init_from_config_file(self, config_file_path):
        pass

# @singleton
class OriShareResourceDBConfig(SqlDBConfig):
    def __init__(self):
        SqlDBConfig.__init__(self)

# @singleton
class UserDBConfig(SqlDBConfig):
    def __init__(self):
        SqlDBConfig.__init__(self)


