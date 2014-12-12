# -*- encoding: utf-8 -*-
'''
Created on '2014/12/12'

@author: 'hu'
'''

from flask.templating import render_template
from json import *
from flask import make_response
from flask import request
from werkzeug.wrappers import Response, Headers
import simplejson
from wxLib.meta.voteMeta import *
from wxLib.utils import *
from wxLib.callws.ehr import *
from sqlalchemy import and_, or_, func
import os
from encoder import XML2Dict
from conf.weixinMenuConf import *
from xml.dom import minidom
import pycurl, StringIO, Cookie
import time


@app.route('/imageView/<src>')
def getImageView(src=None):
    src = '/static/image/' + src
    return render_template('common/imageView.html', src=src)


@app.route('/summary')
def getSummary():
    return render_template('weixin/location_new.html')


@app.route('/business')
def getBussiness():
    return render_template('weixin/business.html')


@app.route('/links')
def getLinks():
    return render_template('weixin/links.html')


@app.route('/weixinrec', methods=['GET', 'POST'])
def weixinrec():
    if request.method == 'GET':
        return request.args.get('echostr')
    xml2dict = XML2Dict(coding='utf-8')
    xml = xml2dict.parse(request.data)
    vo = xml['xml']
    if vo.has_key('Event') and vo.has_key('EventKey'):
        if vo['Event'] == 'CLICK':
            doc = minidom.Document()
            root = doc.createElement('xml')
            doc.appendChild(root)
            toUserName = doc.createElement('ToUserName')
            toUserName.appendChild(doc.createTextNode('<![CDATA[' + vo['FromUserName'] + ']]>'))
            root.appendChild(toUserName)

            fromUserName = doc.createElement('FromUserName')
            fromUserName.appendChild(doc.createTextNode(r'<![CDATA[' + vo['ToUserName'] + r']]>'))
            root.appendChild(fromUserName)

            createTime = doc.createElement('CreateTime')
            createTime.appendChild(doc.createTextNode(r'<![CDATA[' + str(int(time.time() * 1000)) + r']]>'))
            root.appendChild(createTime)

            msgType = doc.createElement('MsgType')
            msgType.appendChild(doc.createTextNode(r'<![CDATA[news]]>'))
            root.appendChild(msgType)

            articles = doc.createElement('Articles')

            for k, group in groups.iteritems():
                if group['name'] == vo['EventKey']:
                    menuHeader = doc.createElement('item')
                    headerTitle = doc.createElement('Title')
                    headerTitle.appendChild(doc.createTextNode(r'<![CDATA[' + group['title'] + r']]>'))
                    menuHeader.appendChild(headerTitle)

                    headerPicUrl = doc.createElement('PicUrl')
                    headerPicUrl.appendChild(doc.createTextNode(r'<![CDATA[' + group['picurl'] + r']]>'))
                    menuHeader.appendChild(headerPicUrl)

                    articles.appendChild(menuHeader)
                    articleNum = 1
                    for k, menu in menus.iteritems():
                        if menu['group'] == group:
                            menuitem = doc.createElement('item')

                            itemTitle = doc.createElement('Title')
                            itemTitle.appendChild(doc.createTextNode(r'<![CDATA[' + menu['title'] + r']]>'))
                            menuitem.appendChild(itemTitle)

                            itemUrl = doc.createElement('Url')
                            itemUrl.appendChild(doc.createTextNode(r'<![CDATA[' + menu['url'] + r']]>'))
                            menuitem.appendChild(itemUrl)

                            itemPicUrl = doc.createElement('PicUrl')
                            itemPicUrl.appendChild(doc.createTextNode(r'<![CDATA[' + menu['picurl'] + r']]>'))
                            menuitem.appendChild(itemPicUrl)

                            articles.appendChild(menuitem)
                            articleNum = articleNum + 1

                    articleCount = doc.createElement('ArticleCount')
                    articleCount.appendChild(doc.createTextNode(str(articleNum)))
                    root.appendChild(articleCount)
                    root.appendChild(articles)
                    xml = str(doc.toxml())
                    xml = xml.replace('&lt;', '<').replace('&gt;', '>')
                    return xml
    return 'error'


def getAccessToken():
    curl = pycurl.Curl()
    f = StringIO.StringIO()
    curl.setopt(pycurl.URL, "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid="
                + APP_ID + "&secret=" + SECRET)
    curl.setopt(pycurl.WRITEFUNCTION, f.write)
    curl.setopt(pycurl.SSL_VERIFYPEER, 0)
    curl.setopt(pycurl.SSL_VERIFYHOST, 0)
    curl.perform()
    backinfo = ''
    if curl.getinfo(pycurl.RESPONSE_CODE) == 200:
        backinfo = f.getvalue()
    curl.close()
    if backinfo=='':
        return False

    result = loads(backinfo)
    return result


if __name__ == '__main__':
    getAccessToken()
    pass