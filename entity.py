# -*- coding: utf-8 -*-

import time
import datetime

from core.base import BaseEntity

class UserResource(BaseEntity):
    def __init__(self, userId=0,
                 shareResourceId="", parentShareResourceId="", available=True, resourceType=0, name="",
                 fileGuid="", fileSize=0, classId=1, subjectCode="", createUserId=1, createTime=datetime.datetime.now(),
                 updateTime=datetime.datetime.now(), syncTime=datetime.datetime.now(), isAllowAppendFile=True):
        BaseEntity.__init__(self)
        self._class = "com.fcr.shareresource.domain.entity.UserResource"
        self.userId = userId
        self.shareResourceId = shareResourceId
        self.parentShareResourceId = parentShareResourceId
        self.available = available
        self.resourceType = resourceType
        self.name = name
        self.fileGuid = fileGuid
        self.fileSize = fileSize
        self.classId = classId
        self.subjectCode = subjectCode
        self.createUserId = createUserId
        self.createTime = createTime
        self.updateTime = updateTime
        self.syncTime = syncTime
        self.isAllowAppendFile = isAllowAppendFile

        self.isTransfer = True

    def fill_resource(self, share_resource):
        self.shareResourceId = share_resource.gid
        self.parentShareResourceId = share_resource.parentId
        self.available = share_resource.available
        self.resourceType = share_resource.resourceType
        self.name = share_resource.name
        self.fileGuid = share_resource.fileGuid
        self.fileSize = share_resource.fileSize
        self.classId = share_resource.classId
        self.subjectCode = share_resource.subjectCode
        self.createUserId = share_resource.createUserId
        self.createTime = share_resource.createTime
        self.updateTime = share_resource.updateTime
        self.syncTime = share_resource.syncTime
        self.isAllowAppendFile = share_resource.isAllowAppendFile

        pass


class ShareResource(BaseEntity):
    def __init__(self,
                 gid="", parentId="", sharedLevel=0, available=True, resourceType=0, name="",
                 fileGuid="", fileSize=0, classId=1, subjectCode="", createUserId=1, createTime=datetime.datetime.now(),
                 updateTime=datetime.datetime.now(), syncTime=datetime.datetime.now(), isAllowAppendFile=True):
        BaseEntity.__init__(self)
        self._class = "com.fcr.shareresource.domain.entity.ShareResource"
        self.gid = gid
        self.parentId = parentId
        self.sharedLevel = sharedLevel
        self.available =available
        self.resourceType = resourceType
        self.name = name
        self.fileGuid = fileGuid
        self.fileSize = fileSize
        self.classId = classId
        self.subjectCode = subjectCode
        self.createUserId =createUserId
        self.createTime = createTime
        self.updateTime =updateTime
        self.syncTime = syncTime
        self.isAllowAppendFile = isAllowAppendFile

        self.isTransfer=True

    def time_path(self):
        self.createTime.astimezone()
    def author_resource(self):
        user_resource = UserResource(userId=self.createUserId)
        user_resource.fill_resource(self)

        return user_resource

    def share_to_users(self, user_ids=[]):
        user_resources = []
        if len(user_ids)<=0:
            return user_resources

        for user_id in user_ids:
            user_resource = UserResource(userId=user_id)
            user_resource.fill_resource(self)
            user_resources.append(user_resource)

        return user_resources


class ExRecord(BaseEntity):

    def __init__(self,record_id=0,message=''):
        BaseEntity.__init__(self)
        self.record_id=record_id
        self.message=message
        self.messages=[]


class ExRecordList:

    def __init__(self):
        self.ids=[]
        self.datas={}


    def add(self,record_id=0,message=''):
        if record_id not in self.ids:
            self.ids.append(record_id)
            self.datas[record_id]=ExRecord(record_id,message)
        else:
            self.datas[record_id].messages.append(message)

    def size(self):
        return len(self.ids)





