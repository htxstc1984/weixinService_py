# -*- encoding: utf-8 -*-
'''
Created on '2015/3/10'

@author: 'hu'
'''

import schedule
import time


def addSchedule(t, func, *args, **kwargs):
    schedule.every().day.at(t).do(func, *args, **kwargs)

# schedule.every(10).seconds.do(test)
# schedule.every().day.at('09:51').do(test)
# schedule.every().day.at('09:53').do(test)



if __name__ == '__main__':
    pass