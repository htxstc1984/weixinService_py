# -*- encoding: utf-8 -*-
'''
Created on '2014/12/3'

@author: 'hu'
'''

from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.types import *
from json import *
from datetime import *
# from globalVars import *
from sqlalchemy import *
import re


class MetaTransform():
    @classmethod
    def getStrInstance(cls, db, **kwargs):
        newkvaggs = dict()
        columns = db.metadata.tables[cls.__tablename__].columns
        for k, v in kwargs.iteritems():
            if isinstance(v, list):
                v = v[0]
            if columns.has_key(k):
                if isinstance(columns[k].type, Integer) or isinstance(columns[k].type, BigInteger) or isinstance(
                        columns[k].type, SmallInteger):
                    if not v.strip() == '':
                        newkvaggs[k] = int(v.strip())
                else:
                    newkvaggs[k] = v
        return cls(**newkvaggs)


class CJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.datedate):
            return obj.strftime('%Y-%m-%d')
        else:
            return JSONEncoder.default(self, obj)


def dict2JsonStr(obj):
    newObj = dict({k: str(v) for k, v in obj.iteritems()})
    return newObj


def sa_obj_to_dict(obj, filtrate=None, rename=None):
    """
    sqlalchemy 对象转为dict
    :param filtrate: 过滤的字段
    :type filtrate: list or tuple
    :param rename: 需要改名的,改名在过滤之后处理, key为原来对象的属性名称，value为需要更改名称
    :type rename: dict
    :rtype: dict
    """

    if isinstance(obj.__class__, DeclarativeMeta):
        # an SQLAlchemy class
        # 该类的相关类型，即直接与间接父类
        cla = obj.__class__.__mro__
        # 过滤不需要的父类
        cla = filter(lambda c: hasattr(c, '__table__'), filter(lambda c: isinstance(c, DeclarativeMeta), cla))
        columns = []
        map(lambda c: columns.extend(c.__table__.columns), cla[::-1])
        # columns = obj.__table__.columns
        if filtrate and isinstance(filtrate, (list, tuple)):
            fields = dict(
                map(lambda c: (c.name, getattr(obj, c.name)), filter(lambda c: not c.name in filtrate, columns)))
        else:
            fields = dict(map(lambda c: (c.name, getattr(obj, c.name)), columns))
        # fields = dict([(c.name, getattr(obj, c.name)) for c in obj.__table__.columns])
        if rename and isinstance(rename, dict):
            # 先移除key和value相同的项
            _rename = dict(filter(lambda (k, v): str(k) != str(v), rename.iteritems()))
            # 如果原始key不存在，那么新的key对应的值默认为None
            # 如果新的key已存在于原始key中，那么原始key的值将被新的key的值覆盖
            # map(lambda (k, v): fields.setdefault(v, fields.pop(k, None)), _rename.iteritems())
            map(lambda (k, v): fields.update({v: fields.pop(k, None)}), _rename.iteritems())
        #
        return fields
    else:
        return {}


##过滤HTML中的标签
# 将HTML中标签等信息去掉
# @param htmlstr HTML字符串.
def filter_tags(htmlstr):
    # 先过滤CDATA
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_br = re.compile('<br\s*?/?>')  # 处理换行
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    s = re_cdata.sub('', htmlstr)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_br.sub('\n', s)  # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    # 去掉多余的空行
    blank_line = re.compile('\n+')
    s = blank_line.sub('\n', s)
    s = replaceCharEntity(s)  #替换实体
    return s


##替换常用HTML字符实体.
# 使用正常的字符替换HTML中特殊的字符实体.
# 你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
#@param htmlstr HTML字符串.
def replaceCharEntity(htmlstr):
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }

    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(htmlstr)
    while sz:
        entity = sz.group()  #entity全称，如&gt;
        key = sz.group('name')  #去除&;后entity,如&gt;为gt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            #以空串代替
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr


def repalce(s, re_exp, repl_string):
    return re_exp.sub(repl_string, s)


def truncate_html(name, length=200):
    #print filter_tags(name)
    suffix = ''
    if len(name) > length:
        suffix = '...'
    result = filter_tags(name)[0:length]
    return result + suffix


if __name__ == '__main__':
    pass