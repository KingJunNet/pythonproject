# -*- coding: utf-8 -*-
from core.mongo_plus import OriShareResourceDBConfig
from time_util import *
from sql_db_client import MsDBClient,AzureDBClient
from cfg_helper import ori_share_resource_db_config

# ori_share_resource_db_config= OriShareResourceDBConfig()
# db_client = MsDBClient(host=ori_share_resource_db_config.host,
#                        user=ori_share_resource_db_config.user,
#                        pwd=ori_share_resource_db_config.pwd,
#                        db=ori_share_resource_db_config.db_name)



def db_client():
    db_config = OriShareResourceDBConfig()
    db_client_obj = AzureDBClient(host=db_config.host,
                              user=db_config.user,
                              pwd=db_config.pwd,
                              db=db_config.db_name)
    return db_client_obj

def load_share_resourcesA(class_id, begin_time, end_time, page_index, page_size):
    datas = []

    row_begin = page_size * (page_index - 1)
    row_end = page_size * page_index
    datas = db_client().ExecQuery("SELECT * FROM("
                                " SELECT  ROW_NUMBER() OVER(ORDER BY Id ASC) AS ROWID,*"
                                " FROM [dbo].[res_ShareResources]"
                                " WHERE ClassId = " + str(class_id) +
                                " AND CreateTime >=" + time_sql_condition(begin_time) +
                                " AND CreateTime < " + time_sql_condition(end_time)+") AS TEMP"
                                " WHERE ROWID > " + str(row_begin) + " AND ROWID <=" + str(row_end))

def load_share_resources(class_id, begin_time, end_time, page_index, page_size):
    datas = []

    row_begin = page_size * (page_index - 1)
    row_end = page_size * page_index
    datas = db_client().ExecQuery("SELECT R.ROWID,"
                                "R.Id,R.Guid,R.Name,R.SubjectCode,R.FileGuid,R.UserId,R.ClassId,"
                                "R.Available,R.UpdateTime,R.CreateTime,R.ResourceType,"
                                "R.ParentId,R.CanAppendChild,R.SyncTime,R.Permission,R.Size,S.Guid"
                                " From (SELECT * FROM("
                                " SELECT  ROW_NUMBER() OVER(ORDER BY Id ASC) AS ROWID,*"
                                " FROM [dbo].[res_ShareResources]"
                                " WHERE Available=1 AND  ClassId = " + str(class_id) +
                                " AND CreateTime >=" + time_sql_condition(begin_time) +
                                " AND CreateTime < " + time_sql_condition(end_time) + ") AS TEMP"
                                " WHERE ROWID > " + str(row_begin) + " AND ROWID <=" + str(row_end) +
                                ") R LEFT JOIN [dbo].[res_ShareResources] S ON R.ParentId=S.Id")

    return datas

def get_share_resource_count(class_id, begin_time, end_time):
    count=0

    datas = db_client().ExecQuery("SELECT COUNT(Id)"                              
                                " FROM [dbo].[res_ShareResources]"                        
                                " WHERE Available=1 AND  ClassId = " + str(class_id) +
                                " AND CreateTime >= " + time_sql_condition(begin_time) +
                                " AND CreateTime < " + time_sql_condition(end_time))
    count=datas[0][0]

    return count

def get_share_resource_guid(ids):
    datas = []

    in_query = build_in_query_sql(ids)
    datas = db_client().ExecQuery(
        "SELECT Id,Guid FROM res_ShareResources"
        " WHERE Id IN " + in_query)

    return datas

def load_class_ids(begin_time, end_time):
    datas = []

    datas = db_client().ExecQuery(
        "SELECT DISTINCT(ClassId) FROM [dbo].[res_ShareResources]"
        " WHERE CreateTime < " + time_sql_condition(end_time) +
        " AND CreateTime >= " + time_sql_condition(begin_time))

    return datas

def time_sql_condition(time_value):
    return "'%s'" % (time2string(time_value))

def build_in_query_sql(ids=[]):
    # 拼接查IN查询条件
    in_query = '('
    for id in ids:
        in_query = in_query  + str(id) + ","
    in_query = in_query[0:(len(in_query)-1)]
    in_query = in_query + ')'

    return in_query

#test
# # from_time=DateTime.try_parse('2001-01-01')
# # to_time=DateTime.try_parse('2020-01-01')
# # load_class_ids(from_time,to_time)
# #get_share_resource_count(7157,from_time,to_time)
# load_share_resources(7157,from_time,to_time,1,10)

# get_share_resource_guid([5286,5301])
