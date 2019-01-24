# -*- coding: utf-8 -*-
from core.db_config import SqlDBConfig
from core.sql_db_client import AzureDBClient,MsDBClient


def sql_sesson(db_config=SqlDBConfig(),is_azure=True):
    db_client=None
    if is_azure:
        db_client = AzureDBClient(host=db_config.host,
                              user=db_config.user,
                              pwd=db_config.pwd,
                              db=db_config.db_name)
    else:
        db_client = MsDBClient(host=db_config.host,
                                  user=db_config.user,
                                  pwd=db_config.pwd,
                                  db=db_config.db_name)

    return db_client

def build_in_query_sql(ids=[]):
    # 拼接查IN查询条件
    in_query = '('
    for id in ids:
        in_query = in_query  + str(id) + ","
    in_query = in_query[0:(len(in_query)-1)]
    in_query = in_query + ')'

    return in_query


