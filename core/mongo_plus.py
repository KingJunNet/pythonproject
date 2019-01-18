# -*- coding: utf-8 -*-
from pymongo import MongoClient
from core.singleton import singleton

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

@singleton
class OriShareResourceDBConfig(SqlDBConfig):
    def __init__(self):
        SqlDBConfig.__init__(self)

@singleton
class UserDBConfig(SqlDBConfig):
    def __init__(self):
        SqlDBConfig.__init__(self)

@singleton
class MongoServiceConfig:
    def __init__(self):
        self.ip = ''
        self.port = 0
        self.db_name = ''
        self.user = ''
        self.pwd = ''

    def init(self,ip='',port=0,db_name='',user='',pwd=''):
        self.ip = ip
        self.port = port
        self.db_name = db_name
        self.user = user
        self.pwd = pwd

    def init_from_config_file(self,config_file_path):
        pass


# #test
# # 加载mongo数据库配置
# mongo_conf = MongoServiceConfig()
# mongo_conf.init(ip='192.168.200.199', port=27017, db_name='FcrShareResourceDBTransfer', user='', pwd='')
#
# class TestData(BaseEntity):
#     def __init__(self, userId=0):
#         BaseEntity.__init__(self)
#         self._class = "com.fcr.shareresource.domain.entity.UserResource"
#         self.userId = userId
#
# data=TestData(2)
# base_repository=BaseRepository()
# base_repository.add(data)