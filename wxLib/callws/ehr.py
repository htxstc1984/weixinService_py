# -*- encoding: utf-8 -*-
'''
Created on '2014/12/10'

@author: 'hu'
'''

from suds.client import Client
from conf.globalConf import *
import simplejson
from json import *
import copy
from operator import *

client = Client(EHR_WSDL_URI)


def checkOpenid(openid):
    localClient = copy.copy(client)
    result = localClient.service.checkOpenId(openid)
    result = localClient.dict(result)
    # result = simplejson.loads(result)
    return result


def getPsnPhoneVOs(openid, cond):
    localClient = copy.copy(client)
    # print localClient
    result = localClient.service.getPsnPhoneVOs(openid, cond)
    # i = unicode(result).find(u'您无此操作权限')
    # if not i == -1:
    #     return dict(code=999, msg='您无此操作权限')
    result = loads(result)
    return result


def bindWeixin(cond, type, openid):
    localClient = copy.copy(client)
    result = localClient.service.bindWeixin(cond, type, openid)
    return result


def unbindWeixin(openid):
    localClient = copy.copy(client)
    result = localClient.service.unbindWeixin(openid)
    return result


def confirmBind(code):
    localClient = copy.copy(client)
    result = localClient.service.confirmBind(code)
    return result


def confirmBindMMS(mmscode, openid):
    localClient = copy.copy(client)
    result = localClient.service.confirmBindMMS(mmscode, openid)
    return result


if __name__ == '__main__':
    print checkOpenid(u'oGWhot6q83jPLENglsitEv1xjYCw')
    # print getPsnPhoneVOs(u'oGWhot6q83jPLENglsitEv1xjYCw', u'黄玉')

    # print  bindWeixin('13950002585','mms','oGWhot6q83jPLENglsitEv1xjYCw')
