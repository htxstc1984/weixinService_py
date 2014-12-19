# -*- encoding: utf-8 -*-
'''
Created on '2014/12/2'

@author: 'hu'
'''

from flask import Flask
from datetime import timedelta
from wxLib.utils import *
import os


try:
    app = Flask(__name__)
    app.debug = True

    ##修改jinja模板的变量引用前后缀
    temp_env = app.jinja_env
    temp_env.variable_start_string = '{&'
    temp_env.variable_end_string = '&}'
    ##增加中文过滤器
    temp_env.filters['truncate_html'] = truncate_html
    ##使用session 包装cookie实现的，没有session id
    app.secret_key = 'daf78s9df7saofjho'
    # 过期时间,通过cookie实现的
    from datetime import timedelta
    app.permanent_session_lifetime = timedelta(minutes=5)

except BaseException, e:
    print e.message

if __name__ == '__main__':
    pass