# -*- coding: utf-8 -*-

from properties import *

def load_db_config(env):
    return {
        "ori_share_resource_db_config": ori_share_resource_db_config(env),
        "user_db_config": user_db_config(env),
        "share_resource_db_config": share_resource_db_config(env),
    }

def ori_share_resource_db_config(env):
    if env == 0:
        return ori_share_resource_db_config_dev
    if env == 1:
        return ori_share_resource_db_config_qa
    if env == 2:
        return ori_share_resource_db_config_production

def user_db_config(env):
    if env == 0:
        return user_db_config_production_dev
    if env == 1:
        return user_db_config_production_qa
    if env == 2:
        return user_db_config_production_production

def share_resource_db_config(env):
    if env == 0:
        return share_resource_db_config_dev
    if env == 1:
        return share_resource_db_config_qa
    if env == 2:
        return share_resource_db_config_production

