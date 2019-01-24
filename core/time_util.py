# -*- coding: utf-8 -*-
import time
import datetime

CONST_DEFAULT_TIME_FOMAT = "%Y-%m-%d %H:%M:%S"

class DateTime:
    @staticmethod
    def to_string(time=datetime.datetime.now()):
        return time2string(time)

    @staticmethod
    def try_parse(time_str):
        try:
            return string2localtime(time_str)
        except Exception,ex:
            return False

    @staticmethod
    def timezone8(time=datetime.datetime.now()):
        delta = datetime.timedelta(hours=8)
        result_time = time - delta
        return result_time

def time2string(time=datetime.datetime.now()):
   return time.strftime(CONST_DEFAULT_TIME_FOMAT)

def string2localtime(time_str):
    return datetime.datetime.strptime(time_str, CONST_DEFAULT_TIME_FOMAT)

