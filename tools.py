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
from decorator import timeit

import tushare as ts
import time, traceback


result = ts.trade_cal()
df = result[(result.calendarDate >= '2018-01-01') & (result.isOpen == 1)]
df2 = result[(result.calendarDate >= '2017-12-01') & (result.calendarDate <= '2018-01-01') & (result.isOpen == 1)] .iloc[-1:].append(df)
trading_day_df = df2.reset_index(drop=True)[['calendarDate']]

def get_3(day):
    ###  获取今日涨停股票的数量
    sql = "select count(*) as num from daily_result_detail where date = '%s' and close_is_raiselimit = 1;" % day
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
    sql = "select count(*) as num from daily_result_detail where date = '%s' and close_is_one = 0 and close_is_raiselimit = 1;" % day
    num_df = pd.read_sql(sql, mysql_engine)
    print(num_df['num'][0])
    return num_df['num'][0]

def get_10(day):
    #上一个交易日
    pre_today = get_pro_trading_day(day)
    return pre_today

def get_11(day):
    #高开率=(昨天非一字涨停板在今天是高开的数量)/昨天非一字涨停板的数量
    pre_today = get_pro_trading_day(day)
    fenmu = get_9(pre_today)
    pre_limit_up_info = get_limit_up_detail(0, pre_today, 0)
    fenzi = 0
    # for code_info in pre_limit_up_info:
    for i, row in pre_limit_up_info.iterrows():
        if is_gaokai(row, day):
            fenzi = fenzi+1
            print(fenzi)
    gaokai_chance = round(fenzi/fenmu, 2)
    return gaokai_chance

def get_18(day):
    return get_10(day)

def get_19(day):
    #成功率=收盘价格上涨/昨日非一字板的数量
    pre_today = get_pro_trading_day(day)
    fenmu = get_9(pre_today)
    pre_limit_up_info = get_limit_up_detail(0, pre_today, 0)
    fenzi = 0
    for i, row in pre_limit_up_info.iterrows():
        print(i)
        if is_shangzhang(0, row, day):
            fenzi = fenzi + 1

    success_rate = round(fenzi/fenmu, 2)
    return success_rate

def get_25(day):
    return get_5(day)

def get_26(day):
    return get_10(day)

def get_27(day):
    pre_today = get_pro_trading_day(day)
    fenmu = get_5(pre_today)
    pre_limit_up_info = get_limit_up_detail(1, pre_today, 0)

    fenzi = 0
    for i, row in pre_limit_up_info.iterrows():
        print(i)
        if is_gaokai_sucess(1, row, day):
            fenzi = fenzi + 1

    gaokai_chance = round(fenzi/fenmu, 2)
    return gaokai_chance

def get_28(day):
    #成功率=昨日10:00涨停的收盘价格上涨/昨日10:00之前非一字板的数量
    pre_today = get_pro_trading_day(day)
    fenmu = get_5(pre_today)
    pre_limit_up_info = get_limit_up_detail(1, pre_today, 2)
    fenzi = 0
    for i, row in pre_limit_up_info.iterrows():
        if is_shangzhang(1, row, day):
            fenzi = fenzi + 1
    success_rate = round(fenzi/fenmu, 2)
    return success_rate


def get_elements_28():
    elements_list = []
    day = datetime.now().strftime("%Y-%m-%d")
    selectSql = "SELECT *from daily_28 where trade_date = '%s';" %(day)
    df = pd.read_sql(selectSql, mysql_engine)
    if not df.empty:
        df['trade_date'] = df['trade_date'] .apply(lambda x: x.strftime('%Y-%m-%d'))
        elements_list = df.iloc[[0]].values[0].tolist()[1:]
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

def get_limit_up_detail(is_ten, day, is_one):
    #获取当天涨停股票的内容,包括 股票代码code
    if 0 == is_ten and 0 == is_one:
        #当天非一字涨停板的信息
        sql = "select code,close_price,ten_price from daily_result_detail where date = '%s'  and close_is_one = 0 and close_is_raiselimit = 1;" % day
    elif 0 == is_ten and 1 == is_one:
        #当天一字板的信息
        sql = "select code,close_price,ten_price from daily_result_detail where date = '%s' and close_is_one = 1 and close_is_raiselimit = 1;" % day
    elif 0 == is_ten and 2 == is_one:
        # 当天涨停板的信息（一字板+非一字板）  ？？？？这个地方应该用一个枚举值
        sql = "select code,close_price,ten_price from daily_result_detail where date = '%s' and close_is_raiselimit = 1;" % day
    else:
        sql = "select code,close_price,ten_price from daily_result_detail where date = '%s' and ten_is_raiselimit = 1;" % day

    detail_info = pd.read_sql(sql, mysql_engine)
    return detail_info

def is_shangzhang(is_ten, code_info, day):
    code = code_info['code']
    tmp = get_code_info(is_ten, code, day)
    if 0 == is_ten:
        if (code_info['close_price'] < tmp['now'][0]):
            return True
        else:
            return False
    else:
        if (code_info['ten_price'] < tmp['now'][0]):
            return True
        else:
            return False

def is_gaokai(row, day):
    return is_gaokai_sucess(0, row, day)

def is_sucess(code_info, day):
    return is_gaokai_sucess(0, code_info, day)

def is_gaokai_sucess(is_ten, row, day):
    sql = "select * from `%s` where code = '%s' and trade_time > '09:30:00';" %(day, row['code'])
    tmp = pd.read_sql(sql, mysql_engine)
    if tmp.empty:
        return False
    else:
        if (0 == is_ten):
            if (row['close_price'] < tmp['open'][0]):
                print((row['code']), (row['close_price']), (tmp['open'][0]))
                return True
            else:
                return False
        else:
            if (row['ten_price'] < tmp['open'][0]):
                return True
            else:
                return False

def get_lianxu_limitup(day):
    sql = "select *from daily_result_detail where date = '%s' and num_raiselimit > 1;" % (day)
    detail_info = pd.read_sql(sql, mysql_engine)
    if detail_info.empty:
        return 0
    else:
        return detail_info.shape[0]

def get_code_info(is_ten, code, day):
    if 0 == is_ten:
        #15：00之后的now 就是收盘价了
        sql = "select * from `%s` where code = '%s' and query_time > '15:00:00' limit 1;" %(day, code)
    else:
        sql = "select * from `%s` where code = '%s' and query_time > '09:59:59' limit 1;" %(day, code)
    tmp = pd.read_sql(sql, mysql_engine)
    return tmp

def shangzhang_rate(day):
    #一字开盘,(-&, -2%),[-2%,0),[0,2%),[2%,5%),[5%,+$) 左闭右开的个数
    rate1_num = []
    rate2_num = []
    rate0 = rate1 = rate2 = rate3 = rate4 = rate5 = 0
    rate6 = rate7 = rate8 = rate9 = rate10 = 0

    pre_today = get_pro_trading_day(day)
    limit_up_info = get_limit_up_detail(0, pre_today, 2)
    for i, row in limit_up_info.iterrows():
        # if row['code'] == '600156':
        this_code_today_info = get_code_info(0, row['code'], day)
        rate1_tmp_series = (this_code_today_info['open']-row['close_price'])/row['close_price']
        try:
            print(i)
            rate1_tmp = rate1_tmp_series[0]
            if (this_code_today_info['bid1'][0] == this_code_today_info['now'][0]):
                #一字开盘
                rate0 = rate0+1
            elif(rate1_tmp < -0.02):
                rate1 = rate1+1
            elif(rate1_tmp < 0):
                rate2 = rate2+1
            elif(rate1_tmp < 0.02):
                rate3 = rate3+1
            elif(rate1_tmp < 0.05):
                rate4 = rate4+1
            else:
                rate5 = rate5+1
            rate2_tmp_series = (this_code_today_info['now'] - row['close_price']) / row['close_price']
            rate2_tmp = rate2_tmp_series[0]
            if (0 == this_code_today_info['turnover'][0]):
                rate10 = rate10 + 1
            elif (rate2_tmp < 0):
                rate7 = rate7 + 1
            elif (rate2_tmp < 0.05):
                rate8 = rate8 + 1
            else:
                rate9 = rate9 + 1
        except Exception as e:
            traceback.print_exc()
    ###  rate6 计算的是 今日连板的数量 也就是从daily_result_detail中选出大于2的
    rate6 = get_lianxu_limitup(day)
    rate1_num.extend([rate0, rate1, rate2, rate3, rate4, rate5])
    rate2_num.extend([rate6, rate7, rate8, rate9, rate10])
    return rate1_num, rate2_num

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

def get_today_code_info(day, code):
    #根据股票代码，返回股票名称，打板时间，第几版
    sql = "select * from `%s` where code = '%s' limit 1;" %(day, code)
    tmp = pd.read_sql(sql, mysql_engine)
    print(day, code)
    code_name = tmp['name'][0]
    #打板时间和第几版
    sql = "select time_raiselimit,num_raiselimit from daily_result_detail where date = '%s' and code = '%s';" % (day, code)
    tmp = pd.read_sql(sql, mysql_engine)
    time_raiselimit = tmp['time_raiselimit'].values[0]
    num_raiselimit = tmp['num_raiselimit'].values[0]
    return {'code':code, 'name':code_name, 'time':time_raiselimit, 'frequency':str(num_raiselimit)}

def get_become_worse(day):
    #从 result表中获取闭盘价不是涨停的股票信息
    sql = "select * from daily_result_detail where date = '%s' and close_is_raiselimit = 0;" %(day)
    tmp = pd.read_sql(sql, mysql_engine)
    result_info = []

    for i, row in tmp.iterrows():
        this_code_today_info = get_code_info(0, row['code'], day)
        tmp_code = row['code']
        tmp_name = this_code_today_info['name'].values[0]
        if '\"' in tmp_name:
            tmp_name = tmp_name[1:]
        tmp_chg = (row['close_price'] - this_code_today_info['yst_close'].values[0])/this_code_today_info['yst_close'].values[0]
        tmp_chg = '%.2f' % (tmp_chg*100)
        tmp_dict = {'code':tmp_code, 'name':tmp_name, 'chg':str(tmp_chg)+'%'}
        result_info.append(tmp_dict)
    print(result_info)

    return result_info


if __name__ == '__main__':
    day = '2019-04-11'
    get_become_worse(day)