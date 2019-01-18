# -*- coding: utf-8 -*-

env=0
def set_env(env_code):
    env=env_code

def ori_share_resource_db_config():
    if env == 0:
        return ori_share_resource_db_config_dev
    if env == 1:
        return ori_share_resource_db_config_qa
    if env == 2:
        return ori_share_resource_db_config_production

def user_db_config():
    if env == 0:
        return user_db_config_production_dev
    if env == 1:
        return user_db_config_production_qa
    if env == 2:
        return user_db_config_production_production

ori_share_resource_db_config_dev = {"host": "192.168.200.201",
                                    "user": "sa",
                                    "pwd": "123456aA",
                                    "db": "Test.EastEdu-FCR-Online"}

ori_share_resource_db_config_qa = {"host": "192.168.101.77",
                                    "user": "sa",
                                    "pwd": "123456aA",
                                    "db": "EastEdu-FCR-Online-Test"}

ori_share_resource_db_config_production = {"host": "nqzc7bwosp.database.chinacloudapi.cn",
                                    "user": "dfwdsa@nqzc7bwosp",
                                    "pwd": "Dfwd2016**",
                                    "db": "EastEdu-FCR-Online"}

user_db_config_production_dev = {"host": "192.168.200.202",
                                    "user": "sa",
                                    "pwd": "123456aA",
                                    "db": "WebSeat-Portal-Online-20170803"}

user_db_config_production_qa = {"host": "192.168.101.77",
                                    "user": "sa",
                                    "pwd": "123456aA",
                                    "db": "WebSeat-Portal-Online-20170809"}

user_db_config_production_production = {"host": "mi8xrtf2z2.database.chinacloudapi.cn",
                                    "user": "webseat",
                                    "pwd": "Dfwd011**",
                                    "db": "WebSeat-Portal-Online-20160826"}

