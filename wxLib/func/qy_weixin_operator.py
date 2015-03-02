# -*- encoding: utf-8 -*-
'''
Created on '2015/2/27'

@author: 'hu'
'''

from globalVars import *
import pycurl, StringIO
from wxLib.weixin.common import *
from wxLib.callws.ehr import *

def convert_result_to_chinese(resultset, Class):
    convertedset = list()
    for row in resultset:
        newrow = copy.copy(row)
        # setattr(newrow, field, getattr(newrow, field).encode('latin-1').decode('gbk'))
        convertedset.append(newrow)
    if not Weixin_org.getSimpleDict == None:
        convertedset = [row.getSimpleDict() for row in convertedset]
    else:
        convertedset = [row for row in convertedset]
    return convertedset


def createOrg(org):
    token = getAccessToken(APP_ID_QY, SECRET_QY)
    if token:
        curl = pycurl.Curl()
        f = StringIO.StringIO()
        if org.has_key('id'):
            curl.setopt(pycurl.URL, "https://qyapi.weixin.qq.com/cgi-bin/department/update?access_token=" + token)
        else:
            curl.setopt(pycurl.URL, "https://qyapi.weixin.qq.com/cgi-bin/department/create?access_token=" + token)
        curl.setopt(pycurl.WRITEFUNCTION, f.write)
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        post_data = dumps(org, ensure_ascii=False).encode('utf-8')
        curl.setopt(curl.POSTFIELDS, post_data)
        curl.perform()
        backinfo = ''
        if curl.getinfo(pycurl.RESPONSE_CODE) == 200:
            backinfo = f.getvalue()
        curl.close()
        if backinfo == '':
            print 'error'
        else:
            print backinfo
            return loads(backinfo)


def createPsn(psn, type='create'):
    try:
        token = getAccessToken(APP_ID_QY, SECRET_QY)
        if token:
            curl = pycurl.Curl()
            f = StringIO.StringIO()
            if type == 'create':
                curl.setopt(pycurl.URL, "https://qyapi.weixin.qq.com/cgi-bin/user/create?access_token=" + token)
            else:
                curl.setopt(pycurl.URL, "https://qyapi.weixin.qq.com/cgi-bin/user/update?access_token=" + token)
            curl.setopt(pycurl.WRITEFUNCTION, f.write)
            curl.setopt(pycurl.SSL_VERIFYPEER, 0)
            curl.setopt(pycurl.SSL_VERIFYHOST, 0)
            post_data = dumps(psn, ensure_ascii=False).encode('utf-8')
            curl.setopt(curl.POSTFIELDS, post_data)
            curl.perform()
            backinfo = ''
            if curl.getinfo(pycurl.RESPONSE_CODE) == 200:
                backinfo = f.getvalue()
            curl.close()
            if backinfo == '':
                print 'error'
            else:
                print backinfo
                return loads(backinfo)
    except BaseException, e:
        return {'errcode': 999, 'errmsg': 'error'}


def deleteOrg(token, org_id):
    if token:
        curl = pycurl.Curl()
        f = StringIO.StringIO()
        curl.setopt(pycurl.URL,
                    "https://qyapi.weixin.qq.com/cgi-bin/department/delete?access_token=" + token + "&id=" + str(
                        org_id))
        curl.setopt(pycurl.WRITEFUNCTION, f.write)
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        curl.perform()
        backinfo = ''
        if curl.getinfo(pycurl.RESPONSE_CODE) == 200:
            backinfo = f.getvalue()
        curl.close()
        if backinfo == '':
            print 'error'
        else:
            print backinfo
            return loads(backinfo)


def deletePsn(psn_id):
    token = getAccessToken(APP_ID_QY, SECRET_QY)
    if token:
        curl = pycurl.Curl()
        f = StringIO.StringIO()
        curl.setopt(pycurl.URL,
                    "https://qyapi.weixin.qq.com/cgi-bin/user/delete?access_token=" + token + "&userid=" + str(
                        psn_id))
        curl.setopt(pycurl.WRITEFUNCTION, f.write)
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        curl.perform()
        backinfo = ''
        if curl.getinfo(pycurl.RESPONSE_CODE) == 200:
            backinfo = f.getvalue()
        curl.close()
        if backinfo == '':
            print 'error'
        else:
            print backinfo
            return loads(backinfo)


def deletePsnBat(psnList):
    token = getAccessToken(APP_ID_QY, SECRET_QY)
    if token:
        curl = pycurl.Curl()
        f = StringIO.StringIO()
        curl.setopt(pycurl.URL,
                    "https://qyapi.weixin.qq.com/cgi-bin/user/batchdelete?access_token=" + token)
        curl.setopt(pycurl.WRITEFUNCTION, f.write)
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        post_data = dumps(psnList, ensure_ascii=False).encode('utf-8')
        curl.setopt(curl.POSTFIELDS, post_data)
        curl.perform()
        backinfo = ''
        if curl.getinfo(pycurl.RESPONSE_CODE) == 200:
            backinfo = f.getvalue()
        curl.close()
        if backinfo == '':
            print 'error'
            return {'errcode': 999, 'errmsg': 'error'}
        else:
            print backinfo
            return loads(backinfo)


def getPsnDetail(psnid):
    token = getAccessToken(APP_ID_QY, SECRET_QY)
    if token:
        curl = pycurl.Curl()
        f = StringIO.StringIO()
        curl.setopt(pycurl.URL,
                    "https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token=" + token + "&userid=" + psnid)
        curl.setopt(pycurl.WRITEFUNCTION, f.write)
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        curl.perform()
        backinfo = ''
        if curl.getinfo(pycurl.RESPONSE_CODE) == 200:
            backinfo = f.getvalue()
        curl.close()
        if backinfo == '':
            print 'error'
            return {}
        else:
            ret = loads(backinfo)
            if ret['errcode'] == 0:
                return ret
            else:
                return {}


def getDeptList():
    token = getAccessToken(APP_ID_QY, SECRET_QY)
    if token:
        curl = pycurl.Curl()
        f = StringIO.StringIO()
        curl.setopt(pycurl.URL, "https://qyapi.weixin.qq.com/cgi-bin/department/list?access_token=" + token)
        curl.setopt(pycurl.WRITEFUNCTION, f.write)
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        curl.perform()
        backinfo = ''
        if curl.getinfo(pycurl.RESPONSE_CODE) == 200:
            backinfo = f.getvalue()
        curl.close()
        if backinfo == '':
            print 'error'
        else:
            ret = loads(backinfo)
            if ret['errcode'] == 0:
                return ret['department']
            else:
                return []


def getPsnInfoByCode(code, agentid):
    token = getAccessToken(APP_ID_QY, SECRET_QY)
    if token:
        curl = pycurl.Curl()
        f = StringIO.StringIO()
        curl.setopt(pycurl.URL,
                    'https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token=' + token + '&code=' + code + '&agentid=' + agentid)
        curl.setopt(pycurl.WRITEFUNCTION, f.write)
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        curl.perform()
        backinfo = ''
        if curl.getinfo(pycurl.RESPONSE_CODE) == 200:
            backinfo = f.getvalue()
        curl.close()
        if backinfo == '':
            return {'errcode': 9999}
        else:
            ret = loads(backinfo)
            return ret


def sendMsgToUser(data):
    token = getAccessToken(APP_ID_QY, SECRET_QY)
    if token:
        curl = pycurl.Curl()
        f = StringIO.StringIO()
        curl.setopt(pycurl.URL, "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token)
        curl.setopt(pycurl.WRITEFUNCTION, f.write)
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        post_data = dumps(data, ensure_ascii=False, indent=2)
        curl.setopt(curl.POSTFIELDS, post_data)
        curl.perform()
        backinfo = ''
        if curl.getinfo(pycurl.RESPONSE_CODE) == 200:
            backinfo = f.getvalue()
        curl.close()
        if backinfo == '':
            return {'errcode': 999, 'errmsg': 'error'}
        else:
            ret = loads(backinfo)
            return ret


def getAccessToken(app_id, secret):
    curl = pycurl.Curl()
    f = StringIO.StringIO()
    curl.setopt(pycurl.URL, "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + app_id + "&corpsecret=" + secret)
    curl.setopt(pycurl.WRITEFUNCTION, f.write)
    curl.setopt(pycurl.SSL_VERIFYPEER, 0)
    curl.setopt(pycurl.SSL_VERIFYHOST, 0)
    curl.perform()
    backinfo = ''
    if curl.getinfo(pycurl.RESPONSE_CODE) == 200:
        backinfo = f.getvalue()
    curl.close()
    if backinfo == '':
        return False

    result = loads(backinfo)
    return result['access_token']


def makeSafeUrl(url):
    url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=' \
          + APP_ID_QY + '&redirect_uri=' + url + '&response_type=code&scope=snsapi_base&state=1#wechat_redirect'
    return url

if __name__ == '__main__':
    pass