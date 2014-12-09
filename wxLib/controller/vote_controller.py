# -*- encoding: utf-8 -*-
'''
Created on '2014/12/2'

@author: 'hu'
'''
from flask.templating import render_template
from json import *
from flask import make_response
from flask import request, session
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


@app.route('/schema/view/<schema_id>', methods=['GET', 'POST'])
def getVoteItems(schema_id=None):
    schema = Vote_schema.query.filter_by(id=schema_id).one()
    return render_template('vote/schemaView.html', schema=schema)


@app.route('/schema/add', methods=['GET', 'POST'])
def schemaAdd():
    schema = Vote_schema()
    schema.fromDate = datetime.utcnow()
    schema.toDate = datetime.utcnow()
    return render_template('vote/schemaEdit.html', schema=schema)


@app.route('/schema/edit/<schema_id>', methods=['GET', 'POST'])
def schemaEdit(schema_id=None):
    schema = Vote_schema.query.filter_by(id=schema_id).one()
    return render_template('vote/schemaEdit.html', schema=schema)


@app.route('/schema/save', methods=['GET', 'POST'])
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
    if (schema.id == None):
        schema.createDate = datetime.utcnow()

    if request.files and request.files['picurl']:
        f = request.files['picurl']
        fname = str(datetime.utcnow().strftime('%Y%M%d_%H%M%S%f')) + f.filename[
                                                                     f.filename.rfind('.'):]  # 获取一个安全的文件名，且仅仅支持ascii字符；
        f.save(ROOT_PATH + UPLOAD_FOLDER + fname)
        schema.picurl = UPLOAD_FOLDER + fname
    db_session.merge(schema)
    db_session.commit()
    return "{'sucess':true}"


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
    if request.files and request.files['picurl']:
        f = request.files['picurl']
        fname = str(datetime.utcnow().strftime('%Y%M%d_%H%M%S%f')) + f.filename[
                                                                     f.filename.rfind('.'):]  # 获取一个安全的文件名，且仅仅支持ascii字符；
        f.save(ROOT_PATH + UPLOAD_FOLDER + fname)
        item.picurl = UPLOAD_FOLDER + fname
    db_session.merge(item)
    db_session.commit()
    return "{'sucess':true}"


@app.route('/showImage/<schema_id>')
def showImage(schema_id=None):
    schema = Vote_schema.query.filter_by(id=schema_id).one()
    return render_template('common/showImage.html', src=schema.picurl)


@app.route('/mobi/vote/<schema_id>')
def getVote(schema_id=None):
    schema = Vote_schema.query.filter_by(id=schema_id).one()
    return render_template('vote/mobi/vote.html', schema=schema)


@app.route('/mobi/vote/submit', methods=['POST'])
def submitVote():
    session.has_key('openid')
    data = request.data
    return 'success'


def makeUrl(src):
    return 'http://' + ROOT_PATH + src


def createTree(schemas):
    root = dict({"id": 'root', "text": "全部投票", "state": "closed"})
    schemas_list = list()
    for schema in schemas:
        assert isinstance(schema, Vote_schema)
        schema_dict = dict()
        schema_dict['id'] = schema.id
        schema_dict['text'] = schema.schemaname
        schema_dict['attributes'] = sa_obj_to_dict(schema)
        schemas_list.append(schema_dict)
    root['children'] = schemas_list
    return str(dumps([root], cls=CJsonEncoder))


if __name__ == '__main__':
    pass