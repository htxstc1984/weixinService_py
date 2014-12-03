# -*- encoding: utf-8 -*-
'''
Created on '2014/12/2'

@author: 'hu'
'''
from flask.templating import render_template
from json import *

from wxLib.meta.voteMeta import *
from wxLib.utils import *


@app.route('/voteSetting')
def voteSetting():
    return render_template('vote/setting.html')


@app.route('/getTree', methods=['GET', 'POST'])
def getschematree():
    schemas = Vote_schema.query.all()
    return createTree(schemas)


def createTree(schemas):
    schemas_list = list()
    for schema in schemas:
        assert isinstance(schema, Vote_schema)
        schema_dict = dict()
        schema_dict['id'] = schema.id
        schema_dict['text'] = schema.schemaname
        schema_dict['attributes'] = sa_obj_to_dict(schema)
        schemas_list.append(schema_dict)
    return str(dumps(schemas_list, cls=CJsonEncoder))


if __name__ == '__main__':
    pass