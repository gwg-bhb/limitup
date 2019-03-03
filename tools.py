#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""

@version: 0.1
@author:  quantpy
@file:    tools.py
@time:    2018/4/17 14:29
"""
import pandas as pd
import numpy as np

from config import mysql_engine


from datetime import datetime, date, timedelta

import tushare as ts
import time


result = ts.trade_cal()
df = result[(result.calendarDate >= '2018-01-01') & (result.isOpen == 1)]
df2 = result[(result.calendarDate >= '2017-12-01') & (result.calendarDate <= '2018-01-01') & (result.isOpen == 1)] .iloc[-1:].append(df)
trading_day_df = df2.reset_index(drop=True)[['calendarDate']]


def get_elements():
    elements_list = []
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    today = datetime.now().strftime('%Y-%m-%d')
    today = "2018-10-30"
    ###  获取今日涨停股票的数量
    select_sql = "select *from daily_result_detail where date = '%s';" % today
    limit_up_all = pd.read_sql(select_sql, mysql_engine)
    elements_list.append(today)
    month = str(datetime.now().timetuple().tm_mon)
    day = str(datetime.now().timetuple().tm_mday)
    elements_list.append(month + '/' + day)
    elements_list.append(month + '月' + day + '日')
    elements_list.append(limit_up_all.shape[0])
    return elements_list


def get_last_trading_day(year, month):
    # tm = pd.Timestamp(year=i.year, month=i.month, day=i.day)
    if month == 12:
        year = year + 1
        month = 1
    else:
        month = month + 1
    next_month_1st_day = pd.Timestamp(year=year, month=month, day=1)
    df = trading_day_df[trading_day_df.calendarDate < str(next_month_1st_day)[0:10]].iloc[-1:]
    return pd.Timestamp(df.iloc[-1]['calendarDate'])


def get_pro_trading_day(TradingDay: str):
    index = trading_day_df[trading_day_df.calendarDate==TradingDay].index
    pro_trading_day = trading_day_df.iloc[index-1]['calendarDate'].iloc[0]
    return pro_trading_day


def time2str(tradeTime):
    hour = str(tradeTime.timetuple().tm_hour)
    minute = str(tradeTime.timetuple().tm_min)
    second = str(tradeTime.timetuple().tm_sec)
    return (hour+minute+second)[0:4]


if __name__ == '__main__':
    get_elements()