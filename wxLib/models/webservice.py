# -*- encoding: utf-8 -*-
'''
Created on 2014��11��17��

@author: huangtx
'''
from suds.client import Client

import simplejson

def checkOpenid(openid):
    client = Client('http://172.16.10.107/uapws/service/nc.ws.intf.IPsnService?wsdl')
    result = client.service.checkOpenId(openid)
    print client
#     result = simplejson.loads(result)
    result = Client.dict(result)
    return  result

def getPsnPhoneVOs(openid,cond):
    client = Client('http://172.16.10.107/uapws/service/nc.ws.intf.IPsnService?wsdl')
    result = client.service.getPsnPhoneVOs(openid,cond)
    print client
    result = simplejson.loads(result)
#     result = Client.dict(result)
    print result
    return  result

if __name__ == '__main__':
#     checkOpenid(u'oGWhot5Akal6hBtya9ByTOrmbVpY')
    getPsnPhoneVOs(u'oGWhot5Akal6hBtya9ByTOrmbVpY',u'黄玉')
