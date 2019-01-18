# -*- coding: utf-8 -*-
from core.mongo_pro import MongoSession

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