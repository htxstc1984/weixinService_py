# -*- encoding: utf-8 -*-
'''
Created on '2015/2/4'

@author: 'hu'
'''
from WXBizMsgCrypt import WXBizMsgCrypt
import xml.etree.cElementTree as ET
from conf.weixinMenuConf import *

wxcpt = WXBizMsgCrypt(TOKEN_QY, AESKEY_QY, APP_ID_QY)


def getDecryptMsg(sReqData, sReqMsgSig, sReqTimeStamp, sReqNonce):
    # sReqData = "<xml><ToUserName><![CDATA[wx5823bf96d3bd56c7]]></ToUserName><Encrypt><![CDATA[RypEvHKD8QQKFhvQ6QleEB4J58tiPdvo+rtK1I9qca6aM/wvqnLSV5zEPeusUiX5L5X/0lWfrf0QADHHhGd3QczcdCUpj911L3vg3W/sYYvuJTs3TUUkSUXxaccAS0qhxchrRYt66wiSpGLYL42aM6A8dTT+6k4aSknmPj48kzJs8qLjvd4Xgpue06DOdnLxAUHzM6+kDZ+HMZfJYuR+LtwGc2hgf5gsijff0ekUNXZiqATP7PF5mZxZ3Izoun1s4zG4LUMnvw2r+KqCKIw+3IQH03v+BCA9nMELNqbSf6tiWSrXJB3LAVGUcallcrw8V2t9EL4EhzJWrQUax5wLVMNS0+rUPA3k22Ncx4XXZS9o0MBH27Bo6BpNelZpS+/uh9KsNlY6bHCmJU9p8g7m3fVKn28H3KDYA5Pl/T8Z1ptDAVe0lXdQ2YoyyH2uyPIGHBZZIs2pDBS8R07+qN+E7Q==]]></Encrypt><AgentID><![CDATA[218]]></AgentID></xml>"
    ret, sMsg = wxcpt.DecryptMsg(sReqData, sReqMsgSig, sReqTimeStamp, sReqNonce)
    if ( ret != 0 ):
        return ret,''
    xml_tree = ET.fromstring(sMsg)

    return ret, xml_tree


if __name__ == '__main__':
    pass