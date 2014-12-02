# -*- encoding: utf-8 -*-
'''
Created on 2014年11月12日

@author: huangtx
'''
from flask.app import Flask
from flask.globals import request, session
from flask.helpers import url_for
from werkzeug.utils import redirect
from flask.templating import render_template
app = Flask('itg')
app.static_folder = 'static'

@app.route('/voteSetting')
def voteSetting():
    return render_template('vote/setting.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088, debug=True)