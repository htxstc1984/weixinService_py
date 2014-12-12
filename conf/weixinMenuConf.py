# -*- encoding: utf-8 -*-
'''
Created on '2014/12/12'

@author: 'hu'
'''

APP_ID = 'wxf0364f589da8ea45'
SECRET = 'c9d8f4f5898d4e02fac60a081a9db121'

groups = dict(
    g1=dict(
        name='summary',
        title='欢迎关注厦门国贸',
        picurl='http://59.57.246.46/WeixinService/image/logo4.jpg'
    ),
    g2=dict(
        name='employee',
        title='欢迎关注厦门国贸',
        picurl='http://59.57.246.46/WeixinService/image/logo4.jpg'
    )
)

menus = dict(
    m1001=dict(
        title='国贸概况',
        picurl='http://59.57.246.46/WeixinService/image/gmgl2.png',
        url='http://59.57.246.46/WeixinService/getSummary.html#mp.weixin.qq.com',
        group=groups['g1'],
        index=1
    ),
    m1002=dict(
        title='经营业务',
        picurl='http://59.57.246.46/WeixinService/image/jyyw.png',
        url='http://59.57.246.46/WeixinService/business.html#mp.weixin.qq.com',
        group=groups['g1'],
        index=2
    ),
    m1003=dict(
        title='国贸新闻',
        picurl='http://59.57.246.46/WeixinService/image/gmxw.png',
        url='http://59.57.246.46/WeixinService/getNews.html#mp.weixin.qq.com',
        group=groups['g1'],
        index=3
    ),
    m1004=dict(
        title='员工认证',
        picurl='http://59.57.246.46/WeixinService/image/ygzq.png',
        url='http://59.57.246.46/WeixinService/register.html?openid=%s',
        group=groups['g2'],
        index=4
    ),
    m1005=dict(
        title='通讯录查询',
        picurl='http://59.57.246.46/WeixinService/image/query.png',
        url='http://59.57.246.46/WeixinService/query.html?openid=%s',
        group=groups['g2'],
        index=5
    ),
    m1006=dict(
        title='国贸股价',
        picurl='http://59.57.246.46/WeixinService/image/gmgj.png',
        url='http://59.57.246.46/WeixinService/getStock.html#mp.weixin.qq.com',
        group=groups['g1'],
        index=6
    )
)

buttons = dict(
    button=[
        dict(
            name='关于国贸',
            sub_button=[
                dict(
                    type='view',
                    name='国贸概况',
                    url='http://59.57.246.46/WeixinService/getSummary.html#mp.weixin.qq.com'
                ),
                dict(
                    type='view',
                    name='经营业务',
                    url='http://59.57.246.46/WeixinService/business.html#mp.weixin.qq.com'
                ),
                dict(
                    type='view',
                    name='国贸新闻',
                    url='http://59.57.246.46/WeixinService/getNews.html#mp.weixin.qq.com'
                ),
                dict(
                    type='view',
                    name='国贸股价',
                    url='http://59.57.246.46/WeixinService/getStock.html#mp.weixin.qq.com'
                ),
            ]
        ),
        dict(
            type='click',
            name='员工专区',
            key='employee'
        ),
        dict(
            type='view',
            name='微信链接',
            url='http://59.57.246.46/WeixinService/getLinks.html'
        )
    ]
)

if __name__ == '__main__':
    pass