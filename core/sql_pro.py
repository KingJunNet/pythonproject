# -*- coding: utf-8 -*-
from core.db_config import SqlDBConfig
from core.sql_db_client import AzureDBClient,MsDBClient


def sql_sesson(db_config=SqlDBConfig(),is_azure=False):
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


