# -*- encoding: utf-8 -*-
'''
Created on 2014-11-19

@author: huangtx@itg.net
'''
from flup.server.fcgi import WSGIServer
from flask.app import Flask


def myapp(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['Hello World!\n']

if __name__ == '__main__':
    WSGIServer(myapp,bindAddress=('127.0.0.1',9000)).run()
    
    app = Flask('aaa')
    
    pass