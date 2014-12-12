# -*- encoding: utf-8 -*-
'''
Created on '2014/12/10'

@author: 'hu'
'''

from suds.client import Client
from conf.globalConf import *
import simplejson
import copy

client = Client(EHR_WSDL_URI)

def checkOpenid(openid):
    localClient = copy.copy(client)
    result = localClient.service.checkOpenId(openid)
    result = localClient.dict(result)
    # result = simplejson.loads(result)
    return result


def getPsnPhoneVOs(openid, cond):
    localClient = copy.copy(client)
    result = localClient.service.getPsnPhoneVOs(openid, cond)
    result = simplejson.loads(result)
    return result


if __name__ == '__main__':
    print checkOpenid(u'oGWhot5Akal6hBtya9ByTOrmbVpY')['psnname']
    print getPsnPhoneVOs(u'oGWhot5Akal6hBtya9ByTOrmbVpY', u'黄玉')
