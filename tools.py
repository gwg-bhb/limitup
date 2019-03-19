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

def get_3(day):
    ###  获取今日涨停股票的数量
    sql = "select count(*) as num from daily_result_detail where date = '%s';" % today
    num_df = pd.read_sql(sql, mysql_engine)
    print(num_df['num'][0])
    return num_df['num'][0]

def get_4(day):
    #当天的非一字板，不包括 st
    sql = "select count(*) as num from daily_result_detail where date = '%s' and close_is_one = 0;" % day
    num_df = pd.read_sql(sql, mysql_engine)
    print(num_df['num'][0])
    return num_df['num'][0]

def get_5(day):
    #十点前上板的非一字涨停板,不包括 st
    sql = "select count(*) as num from daily_result_detail where date = '%s' and ten_is_one = 0 and ten_is_raiselimit = 1;" % day
    num_df = pd.read_sql(sql, mysql_engine)
    print(num_df['num'][0])
    return num_df['num'][0]

def get_6(day):
    #手动填写文字
    return "null"

def get_7(day):
    #手动填写文字
    return "null"

def get_8(day):
    #上一个的全部涨停板（上一个交易日）
    sql = "select count(*) as num from daily_result_detail where date = '%s';" % day
    num_df = pd.read_sql(sql, mysql_engine)
    print(num_df['num'][0])
    return num_df['num'][0]

def get_9(day):
    #上一个交易日非一字数量（上一个交易日）
    sql = "select count(*) as num from daily_result_detail where date = '%s' and close_is_one = 0;" % day
    num_df = pd.read_sql(sql, mysql_engine)
    print(num_df['num'][0])
    return num_df['num'][0]

def get_10(day):
    #上一个交易日
    pre_today =  get_pro_trading_day(day)
    return pre_today

def get_11(day):
    #高开率=(昨天非一字涨停板在今天是高开的数量)/昨天非一字涨停板的数量
    pre_today =  get_pro_trading_day(day)
    fenmu = get_9(pre_today)
    pre_limit_up_info = get_limit_up_detail(0, pre_today)
    fenzi = 0
    for code_info in pre_limit_up_info:
        if(is_gaokai(code_info, day)):
            fenzi = fenzi+1

    gaokai_chance = fenzi/fenmu
    return gaokai_chance

def get_18(day):
    return get_10(day)

def get_19(day):
    #成功率=收盘价格上涨/昨日非一字板的数量
    pre_today =  get_pro_trading_day(day)
    fenmu = get_9(pre_today)
    pre_limit_up_info = get_limit_up_detail(0, pre_today)
    fenzi = 0
    for code_info in pre_limit_up_info:
        if (is_shangzhang(0, code_info, day)):
            fenzi = fenzi+1

    success_rate = fenzi/fenmu
    return success_rate

def get_25(day):
    return get_5(day)

def get_26(day):
    return get_10(day)

def get_27(day):
    pre_today =  get_pro_trading_day(day)
    fenmu = get_5(pre_today)
    pre_limit_up_info = get_limit_up_detail(1, pre_today)

    fenzi = 0
    for code_info in pre_limit_up_info:
        if(is_sucess( code_info, day)):
            fenzi=fenzi+1

    gaokai_chance = fenzi/fenmu
    return gaokai_chance

def get_28(day):
    #成功率=昨日10:00涨停的收盘价格上涨/昨日10:00之前非一字板的数量
    pre_today =  get_pro_trading_day(day)
    fenmu = get_5(pre_today)
    pre_limit_up_info = get_limit_up_detail(1, pre_today)
    fenzi = 0
    for code_info in pre_limit_up_info:
        if (is_shangzhang(1, code_info, day)):
            fenzi=fenzi+1
    success_rate = fenzi/fenmu
    return success_rate

def get_elements():
    elements_list = []
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    today = datetime.now().strftime('%Y-%m-%d')
    pre_today = get_pro_trading_day(today)
    element1 = datetime.now().strftime('%m/%d')
    element2 = datetime.now().strftime('%m') + "月" + datetime.now().strftime('%d') + "日"
    
    elements_list.extend([element1, element2])
    # month = str(datetime.now().timetuple().tm_mon)
    # day = str(datetime.now().timetuple().tm_mday)
    #
    # open_shangzhang_num = open_shangzhang_rate(day)
    # close_shangzhang_num = close_shangzhang_rate(day)
    #
    # element_3 = get_3(today)
    # element_4 = get_4(today)
    # element_5 = get_5(today)
    # element_6 = get_6(today)
    # element_7 = get_7(today)
    # element_8 = get_8(pre_today)
    # element_9 = get_9(pre_today)
    # element_10 = get_10(today)
    # element_11 = get_11(today)
    # element_12 = open_shangzhang_num[0]
    # element_13 = open_shangzhang_num[1]
    # element_14 = open_shangzhang_num[2]
    # element_15 = open_shangzhang_num[3]
    # element_16 = open_shangzhang_num[4]
    # element_17 = open_shangzhang_num[5]
    # element_18 = get_18(today)
    # element_19 = get_19(today)
    # element_20 = close_shangzhang_num[0]
    # element_21 = close_shangzhang_num[1]
    # element_22 = close_shangzhang_num[2]
    # element_23 = close_shangzhang_num[3]
    # element_24 = close_shangzhang_num[4]
    # element_25 = get_25(today)
    # element_26 = get_26(today)
    # element_27 = get_27(today)
    # element_28 = get_28(today)
    #
    #
    # elements_list.append(month + '/' + day)
    # elements_list.append(month + '月' + day + '日')
    # # elements_list.append(limit_up_all.shape[0])
    # elements_list.extend([element_3,element_4,element_5,element_6,element_7,element_8,element_9,element_10,element_11,\
    #                       element_12,element_13,element_14,element_15,element_16,element_17,element_18,element_19,\
    #                       element_20,element_21,element_22,element_23,element_24,element_25,element_26,element_27,element_28])

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

def get_limit_up_detail(is_ten, day):
    #获取当天涨停股票的内容,包括 股票代码code
    if 0 == is_ten:
        sql = "select code,close_price,ten_price from daily_result_detail where date = '%s' and close_is_raiselimit = 1;" % day
    else:
        sql = "select code,close_price,ten_price from daily_result_detail where date = '%s' and ten_is_raiselimit = 1;" % day

    detail_info = pd.read_sql(sql, mysql_engine)
    print(detail_info)
    return detail_info

def is_shangzhang(is_ten, code_info, day):
    code = code_info['code']
    sql = "select ts_code,open,close from daily where ts_code = '%s' and trade_date = '%s';" %(code ,day)
    tmp = pd.read_sql(sql, mysql_engine)
    if 0 == is_ten:
        if (code_info['close_price'] < tmp['close']):
            return True
        else:
            return False
    else:
        if (code_info['ten_price'] < tmp['close']):
            return True
        else:
            return False

def is_gaokai(code_info, day):
    return is_gaokai_sucess(1, code_info, day)

def is_sucess(code_info, day):
    return is_gaokai_sucess(0, code_info, day)

def is_gaokai_sucess(is_ten, code_info, day):
    sql = "select code,open_price,close_price from daily_result_detail where code = '%s' and date = '%s';" %(code_info['code'], day)
    tmp = pd.read_sql(sql, mysql_engine)
    if (0 == is_ten):
        if (code_info['close_price'] < tmp['open_price']):
            return True
        else:
            return False
    else:
        if (code_info['ten_price'] < tmp['open_price']):
            return True
        else:
            return False

def get_code_info(is_ten, code, day):
    if 0 == is_ten:
        sql = "select * from tick_daily where code = '%s' and trade_date = '%s' and trade_time > '15:00:00';" %(code, day)
    else:
        sql = "select * from tick_daily where code = '%s' and trade_date = '%s' and trade_time > '09:59:59';" %(code, day)
    tmp = pd.read_sql(sql, mysql_engine)
    print(tmp)
    return tmp

def open_shangzhang_rate(day):
    #一字开盘,(-&, -2%),[-2%,0),[0,2%),[2%,5%),[5%,+$) 左闭右开的个数
    rate_num = []
    rate0 = 0
    rate1 = 0
    rate2 = 0
    rate3 = 0
    rate4 = 0
    rate5 = 0
    pre_today = get_pro_trading_day(day)
    limit_up_info = get_limit_up_detail(0, pre_today)
    for code_info in limit_up_info:
        tmp = get_code_info(0, code_info['code'], day)
        rate_tmp = (tmp['open']-code_info['close_price'])/code_info['close_price']
        if (tmp['bid1'] == tmp['now']):
            #一字开盘
            rate0 = rate0+1
        elif(rate_tmp < -0.02):
            rate1 = rate1+1
        elif(rate_tmp < 0):
            rate2 = rate2+1
        elif(rate_tmp < 0.02):
            rate3 = rate3+1
        elif(rate_tmp < 0.05):
            rate4 = rate4+1
        else:
            rate5 = rate5+1

    rate_num.append(rate0)
    rate_num.append(rate1)
    rate_num.append(rate2)
    rate_num.append(rate3)
    rate_num.append(rate4)
    rate_num.append(rate5)

    return rate_num

def close_shangzhang_rate(day):
    #连板，(-&, 0),[0，5%),[5%,+$),被停牌的数量 左闭右开的数量
    rate_num = []
    rate0 = 0
    rate1 = 0
    rate2 = 0
    rate3 = 0
    rate4 = 0
    pre_today = get_pro_trading_day(day)
    limit_up_info = get_limit_up_detail(0, pre_today)
    for code_info in limit_up_info:
        tmp = get_code_info(0, code_info['code'], day)
        rate_tmp = (tmp['close']-code_info['close_price'])/code_info['close_price']
        if (0 == tmp['turnover']):
            rate4 = rate4+1
        elif (tmp['num_raiselimit'] > 0):
            #连板
            rate0 = rate0+1
        elif(rate_tmp < 0):
            rate1 = rate1+1
        elif(rate_tmp < 0.05):
            rate2 = rate2+1
        else:
            rate3 = rate3+1

    rate_num.append(rate0)
    rate_num.append(rate1)
    rate_num.append(rate2)
    rate_num.append(rate3)
    rate_num.append(rate4)

    return rate_num

def get_pro_trading_day(TradingDay: str):
    index = trading_day_df[trading_day_df.calendarDate==TradingDay].index
    pro_trading_day = trading_day_df.iloc[index-1]['calendarDate'].iloc[0]
    print(pro_trading_day)
    return pro_trading_day

def time2str(tradeTime):
    hour = str(tradeTime.timetuple().tm_hour)
    minute = str(tradeTime.timetuple().tm_min)
    second = str(tradeTime.timetuple().tm_sec)
    return (hour+minute+second)[0:4]

if __name__ == '__main__':
    day = "2018-10-30"
    get_limit_up_detail(0, day)
    # get_elements()