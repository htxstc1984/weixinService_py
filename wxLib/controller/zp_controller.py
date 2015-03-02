# -*- encoding: utf-8 -*-
'''
Created on '2014/12/12'

@author: 'hu'
'''

from globalVars import *
from flask import session
from flask.templating import render_template
import json
from flask import make_response
from flask import request, url_for, redirect
from werkzeug.wrappers import Response, Headers
import simplejson
from wxLib.meta.weixinMeta import *
from wxLib.utils import *
from wxLib.callws.ehr import *
from sqlalchemy import and_, or_, func
import os
from encoder import XML2Dict
from conf.weixinMenuConf import *
from xml.dom import minidom
import pycurl, StringIO
import time as sysTime
from sqlalchemy import *
import re


@app.route('/zp/zhaopin/<modid>')
def getZhaopinView(modid=None):
    return render_template('weixin/zp/zhaopin.html', modid=modid)


@app.route('/zp/develop')
def getDevView():
    return render_template('weixin/zp/develop.html')


if __name__ == '__main__':
    # createButtons()
    pass