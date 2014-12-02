# -*- encoding: utf-8 -*-
'''
Created on '2014/12/2'

@author: 'hu'
'''
from globalVars import *
from wxLib.meta.vote.voteMeta import *
from flask.globals import request, session
from flask.helpers import url_for
from werkzeug.utils import redirect
from flask.templating import render_template
import simplejson as json


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
        # schema_dict['attributes'] = schema
        schemas_list.append(schema_dict)
    return str(json.dumps(schemas_list, sort_keys=True))


if __name__ == '__main__':
    pass