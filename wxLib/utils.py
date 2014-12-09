# -*- encoding: utf-8 -*-
'''
Created on '2014/12/3'

@author: 'hu'
'''

from sqlalchemy.ext.declarative import DeclarativeMeta
from json import *
from datetime import *


class CJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.datedate):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


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
            #先移除key和value相同的项
            _rename = dict(filter(lambda (k, v): str(k) != str(v), rename.iteritems()))
            #如果原始key不存在，那么新的key对应的值默认为None
            #如果新的key已存在于原始key中，那么原始key的值将被新的key的值覆盖
            # map(lambda (k, v): fields.setdefault(v, fields.pop(k, None)), _rename.iteritems())
            map(lambda (k, v): fields.update({v: fields.pop(k, None)}), _rename.iteritems())
        #
        return fields
    else:
        return {}


if __name__ == '__main__':
    pass