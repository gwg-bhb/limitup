#encoding: utf-8

from functools import wraps
from flask import session, redirect, url_for
import pandas as pd

# 登录限制的装饰器
def login_required(func):

    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper


def timeit(func):
    """计时装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        time_start = pd.datetime.now()
        print('%s:' % pd.to_datetime(time_start), func.__name__, 'starts...')
        ret = func(*args, **kwargs)
        time_end = pd.datetime.now()
        print('%s:' % pd.to_datetime(time_end), func.__name__, 'finished.', end=' ')
        print('Total time used: %.2fSec.' % (time_end - time_start).total_seconds(), '\n')

        return ret

    return wrapper