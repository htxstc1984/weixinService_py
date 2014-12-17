# -*- encoding: utf-8 -*-
'''
Created on '2014/12/15'

@author: 'hu'
'''
import pycurl, StringIO
from json import *


def test(url):
    try:
        crl = pycurl.Curl()
        crl.setopt(pycurl.VERBOSE, 1)
        crl.setopt(pycurl.FOLLOWLOCATION, 1)
        crl.setopt(pycurl.MAXREDIRS, 5)
        # crl.setopt(pycurl.AUTOREFERER,1)
        crl.setopt(pycurl.HTTPHEADER,['Content-Type:text/html'])
        crl.setopt(pycurl.CONNECTTIMEOUT, 60)
        crl.setopt(pycurl.TIMEOUT, 300)
        # crl.setopt(pycurl.PROXY,proxy)
        crl.setopt(pycurl.HTTPPROXYTUNNEL, 1)
        #crl.setopt(pycurl.NOSIGNAL, 1)
        crl.fp = StringIO.StringIO()
        crl.setopt(pycurl.USERAGENT, "dhgu hoho")

        content = '<xml>'
        content += '<ToUserName><![CDATA[toUser]]></ToUserName>'
        content += '<FromUserName><![CDATA[oGWhot6q83jPLENglsitEv1xjYCw]]></FromUserName>'
        content += '<CreateTime>1348831860</CreateTime>'
        content += '<MsgType><![CDATA[event]]></MsgType>'
        content += '<Event><![CDATA[CLICK]]></Event>'
        content += '<EventKey><![CDATA[employee]]></EventKey>'
        # + "<Content><![CDATA[投票]]></Content>"
        # + "<MsgId>1234567890123456</MsgId>"
        content += '</xml>'
        # Option -d/--data <data> HTTP POST data
        crl.setopt(crl.POSTFIELDS, content)
        f = StringIO.StringIO()
        crl.setopt(pycurl.URL, url)
        crl.setopt(crl.WRITEFUNCTION, f.write)
        crl.perform()

        backinfo = ''
        if crl.getinfo(pycurl.RESPONSE_CODE) == 200:
            backinfo = f.getvalue()
        crl.close()
        print backinfo
    except BaseException, e:
        print e.message


if __name__ == '__main__':
    print test("http://localhost:8088/weixinrec")
    # print test('http://59.57.246.46/WeixinService/weixinrec.html')
    # print test('http://172.16.109.105:8080/WeixinService/weixinrec.html')
    pass