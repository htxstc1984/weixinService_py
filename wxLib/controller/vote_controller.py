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
import simplejson
from wxLib.meta.voteMeta import *
from wxLib.utils import *
from wxLib.callws.ehr import *
from sqlalchemy import and_, or_, func
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
    schema = Vote_schema.getStrInstance(**request.form)
    schema.creator = u'htx'
    schema.lastDate = unicode(datetime.utcnow())
    if (schema.id == None):
        schema.createDate = unicode(datetime.utcnow())

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
    item = Vote_item.getStrInstance(**request.form)
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


@app.route('/mobi/vote/<schema_id>/<openid>')
def getVote(schema_id=None, openid=None):
    if openid == None:
        if session.has_key('openid'):
            openid = session.get('openid')
        else:
            return render_template('vote/error.html', title=u'错误', message=u'无法确认您的微信身份')
    rs = checkOpenid(openid)
    if rs['resultCode'] != 0:
        return render_template('vote/error.html', title=u'错误', message=u'无法确认您的微信身份')
    session['openid'] = openid
    schema = Vote_schema.query.filter_by(id=schema_id).one()
    if schema == None:
        return render_template('vote/error.html', title=u'错误', message=u'您选择的投票不存在')
    items = db_session.query(Vote_item, Vote_action.item_id).outerjoin(Vote_action,
                                                                       Vote_action.item_id == Vote_item.id).filter(
        and_(Vote_item.schema_id == schema.id)).all()

    return render_template('vote/mobi/vote.html', schema=schema, openid=openid, items=items)


@app.route('/mobi/vote/submit', methods=['POST'])
def submitVote():
    if not session.has_key('openid'):
        return render_template('vote/error.html', title=u'错误', message=u'无法确认您的微信身份')
    try:
        openid = session['openid']
        data = request.data
        json = simplejson.loads(data)
        actions = list()

        for selectItem in json['selectItems']:
            action = Vote_action(openid=json['openid'], item_id=int(selectItem), schema_id=json['schema_id'],
                                 voteDate=unicode(datetime.utcnow()))
            actions.append(action)

        oldactions = db_session.query(Vote_action).filter(
            and_(Vote_action.openid == openid, Vote_action.schema_id == json['schema_id'])).all()

        for oldaction in oldactions:
            db_session.delete(oldaction)

        db_session.add_all(actions)
        db_session.commit()
        return str(openid)
    except BaseException, e:
        print e.message
        return 'error'


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