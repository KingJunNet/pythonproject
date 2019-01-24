# -*- coding: utf-8 -*-
import datetime
from core.base import *
from entity import UserResource, ShareResource


class ShareResourceRepository(BaseRepository):
    """
       共享资源仓储
           """
    def __init__(self):
        BaseRepository.__init__(self)

    def batch_delete_by_gid(self,gids=[]):
        query = {'gid': {'$in':gids}}
        result = self.get_collection().delete_many(query)

    def get_collection(self):
        return self.mongo_session.db.ShareResource

class UserResourceRepository(BaseRepository):
    """
           用户资源仓储
               """
    def __init__(self):
        BaseRepository.__init__(self)

    def batch_delete_by_gid(self,gids=[]):
        query = {'shareResourceId': {'$in':gids}}
        result = self.get_collection().delete_many(query)

    def get_collection(self):
        return self.mongo_session.db.UserShareResource

class ExRecordRepository(BaseRepository):
    """
           用户资源仓储
               """
    def __init__(self):
        BaseRepository.__init__(self)

    def get_collection(self):
        return self.mongo_session.db.ExRecord
# #test
# # 加载mongo数据库配置
# mongo_conf = MongoServiceConfig()
# mongo_conf.init(ip='192.168.200.199', port=27017, db_name='FcrShareResourceDBTransfer', user='', pwd='')
#
# share_resource= ShareResource(gid="111", parentId="111", sharedLevel=0, available=True, resourceType=0, name="111",
#                  fileGuid="111", fileSize=0, classId=1, subjectCode="111", createUserId=1, createTime=datetime.datetime.now(),
#                  updateTime=datetime.datetime.now(), syncTime=datetime.datetime.now(), isAllowAppendFile=True)
# repository=ShareResourceRepository()
# repository.add(share_resource)