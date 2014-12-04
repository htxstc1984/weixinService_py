# -*- encoding: utf-8 -*-
'''
Created on '2014/12/2'

@author: 'hu'
'''
from flask.templating import render_template
from json import *
from flask import make_response
from flask import request
from werkzeug.wrappers import Response, Headers
from werkzeug.utils import secure_filename

from wxLib.meta.voteMeta import *
from wxLib.utils import *
import os


@app.route('/voteSetting')
def voteSetting():
    return render_template('vote/setting.html')


@app.route('/getTree', methods=['GET', 'POST'])
def getschematree():
    schemas = Vote_schema.query.all()
    resp = make_response(createTree(schemas))
    assert isinstance(resp, Response)
    resp.headers = Headers({'Content-type': 'application/json'})
    return resp


@app.route('/schemaView/<schemaid>')
def getVoteItems(schemaid=None):
    schema = Vote_schema.query.filter_by(id=schemaid).one()
    return render_template('vote/schemaView.html', schema=schema)


@app.route('/saveSchema', methods=['GET', 'POST'])
def saveSchema():
    schema = Vote_schema()
    schema.id = (request.form['id']) and int(request.form['id']) or schema.id
    schema.schemaname = (request.form['schemaname']) and request.form['schemaname'] or schema.schemaname
    schema.creator = u'htx'
    schema.fromDate = (request.form['fromDate']) and request.form['fromDate'] or schema.fromDate
    schema.toDate = (request.form['toDate']) and request.form['toDate'] or schema.toDate
    schema.desc = (request.form['desc']) and request.form['desc'] or schema.desc
    schema.mutimax = (request.form['mutimax']) and int(request.form['mutimax']) or schema.mutimax
    schema.lastDate = datetime.utcnow()

    if request.files['picurl']:
        f = request.files['picurl']
        fname = str(datetime.utcnow().strftime('%Y%M%d_%H%M%S%f')) + f.filename[
                                                                     f.filename.rfind('.'):]  # 获取一个安全的文件名，且仅仅支持ascii字符；
        f.save(ROOT_PATH + UPLOAD_FOLDER + fname)
        schema.picurl = UPLOAD_FOLDER + fname
    db_session.merge(schema)
    db_session.commit()


@app.route('/item/add/<schema_id>')
def addItem(schema_id=None):
    item = Vote_item(schema_id=schema_id)
    return render_template('vote/itemEdit.html', item=item)


@app.route('/item/edit/<itemid>')
def getItem(itemid=None):
    item = Vote_item.query.filter_by(id=itemid).one()
    return render_template('vote/itemEdit.html', item=item)


@app.route('/item/save', methods=['GET', 'POST'])
def saveItem():
    item = Vote_item(**request.form)
    item.id = (request.form['id']) and int(request.form['id']) or None
    item.schema_id = (request.form['schema_id']) and int(request.form['schema_id']) or None
    if request.files['picurl']:
        f = request.files['picurl']
        fname = str(datetime.utcnow().strftime('%Y%M%d_%H%M%S%f')) + f.filename[
                                                                     f.filename.rfind('.'):]  # 获取一个安全的文件名，且仅仅支持ascii字符；
        f.save(ROOT_PATH + UPLOAD_FOLDER + fname)
        item.picurl = UPLOAD_FOLDER + fname
    db_session.merge(item)
    db_session.commit()


@app.route('/showImage/<src>')
def showImage(src=None):
    render_template('common/showImage.html', src=src)


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