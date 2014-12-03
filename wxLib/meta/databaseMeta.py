# -*- encoding: utf-8 -*-
'''
Created on '2014/12/3'

@author: 'hu'
'''
import os, sys

thePath = os.getcwdu()
thePath = thePath[:thePath.find("weixinService_py\\") + len('weixinService_py')]
sys.path.append(thePath)

from globalVars import *
execfile(os.getcwdu() + "\\voteMeta.py")


if __name__ == '__main__':
    manager.run()
    pass