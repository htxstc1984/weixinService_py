# -*- encoding: utf-8 -*-
'''
Created on '2014/12/12'

@author: 'hu'
'''

APP_ID = 'wxf0364f589da8ea45'
SECRET = 'c9d8f4f5898d4e02fac60a081a9db121'

APP_ID_QY = 'wxeb2ff9ff082f4076'
SECRET_QY = '3oF4yHGkiiIXjm31cnpq-XievtGixoeMTCofruChZyqd97zQQwie0TWcZ5JDEbKi'

groups = dict(
    g1=dict(
        name='summary',
        title='欢迎关注厦门国贸',
        picurl='http://59.57.246.46/static/image/logo4.jpg'
    ),
    g2=dict(
        name='employee',
        title='欢迎关注厦门国贸',
        picurl='http://59.57.246.46/static/image/logo4.jpg'
    ),
    g3=dict(
        name='theme',
        title='欢迎关注厦门国贸',
        picurl='http://59.57.246.46/static/image/logo4.jpg'
    )
)

menus = dict(
    m1001=dict(
        title='国贸概况',
        picurl='http://59.57.246.46/static/image/gmgl2.png',
        url='http://59.57.246.46/summary#mp.weixin.qq.com',
        group=groups['g1'],
        index=1
    ),
    m1002=dict(
        title='经营业务',
        picurl='http://59.57.246.46/static/image/jyyw.png',
        url='http://59.57.246.46/business#mp.weixin.qq.com',
        group=groups['g1'],
        index=2
    ),
    m1003=dict(
        title='国贸新闻',
        picurl='http://59.57.246.46/static/image/gmxw.png',
        url='http://59.57.246.46/news/list/0',
        group=groups['g1'],
        index=3
    ),
    # m1004=dict(
    # title='员工认证',
    # picurl='http://59.57.246.46/static/image/ygzq.png',
    #     url='http://59.57.246.46/register/%s',
    #     group=groups['g2'],
    #     index=4
    # ),
    m1005=dict(
        title='员工专区',
        picurl='http://59.57.246.46/static/image/query.png',
        url='http://59.57.246.46/itg/menus/%s',
        group=groups['g2'],
        index=5
    ),
    m1006=dict(
        title='国贸股价',
        picurl='http://59.57.246.46/static/image/gmgj.png',
        url='http://59.57.246.46/stock#mp.weixin.qq.com',
        group=groups['g1'],
        index=6
    ),
    m1007=dict(
        title='新年送祝福',
        picurl='http://59.57.246.46/static/image/djs.png',
        url='http://59.57.246.46/collect/1/main/%s',
        group=groups['g3'],
        index=7
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
                    url='http://59.57.246.46/summary'
                ),
                dict(
                    type='view',
                    name='经营业务',
                    url='http://59.57.246.46/business'
                ),
                dict(
                    type='view',
                    name='国贸新闻',
                    url='http://59.57.246.46/news/list/0'
                ),
                dict(
                    type='view',
                    name='国贸股价',
                    url='http://59.57.246.46/stock'
                ),
                dict(
                    type='view',
                    name='微信链接',
                    url='http://59.57.246.46/links'
                )

            ]
        ),
        dict(
            type='click',
            name='员工专区',
            key='employee'
        ),
        dict(
            type='click',
            name='新年送祝福',
            key='theme'
        )
    ]
)

errors = dict(
    e101='此微信号已经通过认证，请不要反复认证',
    e102='您锁输入的国贸邮箱不存在，请与IT部联系',
    e103='通过您的姓名和邮箱查到多条记录，请和管理员确认',
    e104='此链接已经失效，无法认证，请重新认证',
    e105='找不到此微信号的认证记录，无需删除',
    e106='未绑定',
    e107='您输入的邮箱已经被绑定，如有疑问请与管理员联系',
    e108='您的微信号已经通过认证，此链接已经失效',
    e109='您输入的手机号码在ehr中找不到或者未加入国贸短信机白名单，请改为邮箱验证',
    e110='短信发送失败',
    e111='此验证码已经失效,请重新验证',
    e112='此手机号在ehr中绑定多个员工，请更换邮箱注册或与管理员联系',
    e113='您发送的未验证的认证请求次数太多，基于安全考虑,无法继续提供此种验证服务，请更换验证方式，或者与管理员联系',
    e114='此验证码已经超时失效',
    e115='您输入的手机号对应的员工已经通过认证，请勿重复认证',
    e999='出现未知错误，操作失败'
)

testCommand = dict(
    zhufu='http://59.57.246.46/collect/1/main/%s'
)

if __name__ == '__main__':
    pass