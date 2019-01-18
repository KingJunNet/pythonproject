# -*- coding: UTF-8 -*-
import logging
import time

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)

# logging.debug("This is a debug log.")
# logging.info("This is a info log.")
# logging.warning("This is a warning log.")
# logging.error("This is a error log.")
# logging.critical("This is a critical log.")

def log_info(message):
    print(message.decode('UTF-8'))
    logging.info(message)

def log_ex(message):
    print(message.decode('UTF-8'))
    logging.exception()

def log_cost(start_time = time.time()):
    # 计算时间差值
    seconds, minutes, hours = int(time.time() - start_time), 0, 0

    # 可视化打印
    hours = seconds // 3600
    minutes = (seconds - hours * 3600) // 60
    seconds = seconds - hours * 3600 - minutes * 60
    log_info("complete time cost {:>02d}:{:>02d}:{:>02d}".format(hours, minutes, seconds))



