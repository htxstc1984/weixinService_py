# -*- encoding: utf-8 -*-
'''
Created on 2014-11-14

@author: huangtx@itg.net
'''

from suds.client import Client
import simplejson

if __name__ == '__main__':
    
    client = Client('http://172.16.10.107/uapws/service/nc.ws.intf.IPsnService?wsdl')
    print client
    result = client.service.getPsnPhoneVOs('oGWhot5Akal6hBtya9ByTOrmbVpY', u'林乐') 
    result = simplejson.loads(result)
    print  result
    
    pass