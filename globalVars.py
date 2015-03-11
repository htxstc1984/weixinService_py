# -*- encoding: utf-8 -*-
'''
Created on '2014/12/2'

@author: 'hu'
'''

from flask import Flask
from datetime import timedelta,datetime
from wxLib.utils import *

from wxLib.meta.weixinMeta import *
from wxLib.meta.ehrMeta import *
from wxLib.meta.itginnerMeta import *
from wxLib.meta.itgcmsMeta import *
from wxLib.meta.mmsMeta import *

import os
import logging
from logging.handlers import RotatingFileHandler
ROOT_PATH = os.path.dirname(__file__)
try:
    app = Flask(__name__)
    app.debug = True

    ##修改jinja模板的变量引用前后缀
    temp_env = app.jinja_env
    temp_env.variable_start_string = '{&'
    temp_env.variable_end_string = '&}'
    ##增加中文过滤器
    temp_env.filters['truncate_html'] = truncate_html
    temp_env.filters['good_display'] = good_display
    ##使用session 包装cookie实现的，没有session id
    app.secret_key = 'daf78s9df7saofjho'
    # 过期时间,通过cookie实现的
    from datetime import timedelta
    app.permanent_session_lifetime = timedelta(minutes=5)

    # file_handler = RotatingFileHandler('tmp/debuglog.log', 'a', 1 * 1024 * 1024, 10)
    # file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    # app.logger.setLevel(logging.INFO)
    # file_handler.setLevel(logging.INFO)
    # app.logger.addHandler(file_handler)
    # app.logger.info('microblog startup')


    # logging.basicConfig()
    # logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

except BaseException, e:
    print e.message

if __name__ == '__main__':
    pass