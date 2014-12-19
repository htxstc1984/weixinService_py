# -*- encoding: utf-8 -*-
'''
Created on 2014年11月12日

@author: huangtx
'''
import os, sys
from globalVars import *

execfile(os.path.dirname(__file__) + "\\wxLib\\controller\\vote_controller.py")
execfile(os.path.dirname(__file__) + "\\wxLib\\controller\\weixin_controller.py")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088, debug=True)