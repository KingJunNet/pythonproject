# -*- coding: UTF-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')
current_working_directory = r"F:\king_project\python_project\fcr.shareresource.datatransfer"
sys.path.append(current_working_directory)
sys.path.append(r"F:\king_project\python_project\fcr.shareresource.datatransfer\venv")
sys.path.append(r"F:\king_project\python_project\fcr.shareresource.datatransfer\venv\Lib")
sys.path.append(r"F:\king_project\python_project\fcr.shareresource.datatransfer\venv\Lib\site-packages")
print sys.path
# from shareresource_repository import ShareResourceRepository, MongoServiceConfig
from handler import *
from cfg_helper import *
from core.db_config import MongoServiceConfig
from cfg_mapper import OriShareResourceDBConfig, UserDBConfig


def main():
    # test
    log_info('数据迁移程序启动中...')
    global_init()
    log_info('数据迁移程序已启动')
    start()
    log_info('数据迁移程序退出')

def start():
    continue_task=True
    while continue_task:
        log_info('开始执行迁移任务')
        from_time=input_from_time()
        to_time=input_to_time(from_time)
        log_info('老铁，迁移任务正在执行，请耐心等待')
        data_handler = DataHandler(begin_time=from_time, end_time=to_time)
        data_handler.work()
        log_info('本次迁移任务结束')
        retry_code = raw_input(u"input Y continue:")
        continue_task= (retry_code == 'Y' or retry_code == 'y')
    else:
        return



def input_from_time():
    retry=True
    from_time=None
    while retry:
        from_time_input = raw_input(u"老铁，请输入起始查询时间，如2017-11-11，请保证格式正确，否则程序可能会爆炸:")
        from_time = DateTime.try_parse(from_time_input)
        if not from_time:
            print u'您输入的时间格式有误，请重新输入'
        else:
            retry = False
    else:
        print u'您输入的起始查询时间是:', DateTime.to_string(from_time)
        return from_time

def input_to_time(from_time):
    retry=True
    to_time=None
    while retry:
        to_time_input = raw_input(u"老铁，请输入截止查询时间，如2017-11-11，请保证格式正确，否则程序可能会爆炸:")
        to_time = DateTime.try_parse(to_time_input)
        if not to_time:
            print u'您输入的时间格式有误，请重新输入'
        elif to_time<=from_time:
            print u'您输入的截止时间小于起始时间，请重新输入'
        else:
            retry = False
    else:
        print u'您输入的截止查询时间是:', DateTime.to_string(to_time)
        return to_time

def input_env():
    env_input = raw_input(u"输入环境变量，dev：0,qa：1,production：2:")
    env = int(env_input)
    return env

def global_init():
    env_code = raw_input(u"输入环境变量，dev：0,qa：1,production：2:")
    env = int(env_code)
    db_cfg_init(env)

def db_cfg_init(env):
    db_cfg= load_db_config(env)

    # "ori_share_resource_db_config": ori_share_resource_db_config(env),
    #     "user_db_config": user_db_config(env),
    #     "share_resource_db_config": share_resource_db_config(env),

    # # 加载mongo数据库配置
    # mongo_conf = MongoServiceConfig()
    # mongo_conf.init(ip='192.168.200.199', port=27017, db_name='FcrShareResourceDBTransferProduction', user='', pwd='')

    # 加载mongo数据库配置
    share_resource_db_config=db_cfg["share_resource_db_config"]
    mongo_conf = MongoServiceConfig()
    mongo_conf.init(ip=share_resource_db_config["host"],
                    port=share_resource_db_config["port"],
                    db_name=share_resource_db_config["db"],
                    user=share_resource_db_config["user"],
                    pwd=share_resource_db_config["pwd"])

    ori_share_resource_db_config_item = db_cfg["ori_share_resource_db_config"]
    ori_share_resource_db_config = OriShareResourceDBConfig()
    ori_share_resource_db_config.init(host=ori_share_resource_db_config_item["host"],
                                      db_name=ori_share_resource_db_config_item["db"],
                                      user=ori_share_resource_db_config_item["user"],
                                      pwd=ori_share_resource_db_config_item["pwd"])

    user_db_config_item = db_cfg["user_db_config"]
    user_db_config = UserDBConfig()
    user_db_config.init(host=user_db_config_item["host"],
                                      db_name=user_db_config_item["db"],
                                      user=user_db_config_item["user"],
                                      pwd=user_db_config_item["pwd"])

main()


























