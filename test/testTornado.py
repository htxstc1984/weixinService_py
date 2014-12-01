# -*- encoding: utf-8 -*-
'''
Created on 2014-11-19

@author: huangtx@itg.net
'''
from tornado import httpserver
from tornado.options import define, options
import tornado.web

define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self,input):
        print input
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')
        


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/(\w+)", IndexHandler)])
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    
    