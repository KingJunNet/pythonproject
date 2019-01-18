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

class MongoSession:
    """
            MongoDB会话对象
            """
    # def __init__(self):
    #     mongo_service_config=MongoServiceConfig()
    #     self._init_db(mongo_service_config.ip,mongo_service_config.port,mongo_service_config.db_name)

    def __init__(self,ip='', port=0, db_name=''):
        if ip=='' and port==0 and db_name=='':
            mongo_service_config = MongoServiceConfig()
            self._init_db(mongo_service_config.ip, mongo_service_config.port, mongo_service_config.db_name)
        else:
            self._init_db(ip,port,db_name)

    def _init_db(self,ip, port, db_name):
        self.ip=ip
        self.port=port
        self.db_name=db_name
        self.connect_str='mongodb://%s:%d'%(ip,port)
        self.mongo_client = MongoClient(self.connect_str)
        self.db = self.mongo_client[db_name]

class JsonConvert:
    """
           Json转换器
           """
    def __init__(self):
        pass

    @staticmethod
    def serialize_object(obj,ignore_fields=[]):
        '''把Object对象转换成Dict对象'''
        dict = {}
        dict.update(obj.__dict__)
        for field in ignore_fields:
            del dict[field]

        return dict

class BaseEntity:
    """
       实体基类
           """
    def __init__(self):
        pass

    def to_json(self):
       return JsonConvert.serialize_object(self, [])

class BaseRepository:
    """
        基础仓储
        """
    def __init__(self):
        self.mongo_session=MongoSession()
        pass

    def add(self,entity= BaseEntity()):
        entity_json = entity.to_json()
        result = self.get_collection().insert_one(entity_json)
        id = str(result.inserted_id)

    def batchAdd(self,entities= [BaseEntity()]):
        entity_jsons=[]
        for entity in entities:
            entity_json = entity.to_json()
            entity_jsons.append(entity_json)
        result = self.get_collection().insert_many(entity_jsons)
        return  result.inserted_ids



    def get_collection(self):
        return self.mongo_session.db.Test


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