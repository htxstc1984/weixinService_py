# -*- encoding: utf-8 -*-
'''
Created on '2015/1/9'

@author: 'hu'
'''

import pycurl
import sys


class Storage:
    def __init__(self):
        self.contents = list()
        self.line = 0

    def store(self, buf):
        self.contents.append(buf)
        # self.line = self.line + 1
        # self.contents = "%s%i: %s" % (self.contents, self.line, buf)

    def __str__(self):
        return self.contents


retrieved_body = Storage()
retrieved_headers = Storage()
c = pycurl.Curl()
c.setopt(c.URL, 'http://www.itg.net/admin/eEdit/uploadfile/201501/20150105172715587.jpg')
c.setopt(c.WRITEFUNCTION, retrieved_body.store)
c.setopt(c.HEADERFUNCTION, retrieved_headers.store)
c.perform()
c.close()
print retrieved_headers
print retrieved_body

if __name__ == '__main__':
    pass