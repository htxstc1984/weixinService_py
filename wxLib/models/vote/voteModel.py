# -*- encoding: utf-8 -*-
'''
Created on '2014/12/2'

@author: 'hu'
'''

from wxLib.meta.voteMeta import *
from datetime import datetime

if __name__ == '__main__':
    item = Vote_item(itemtitle='item1', itemdesc='item1')
    schema = Vote_schema()

    schema.schemaname = u'投票1'
    schema.desc = u'投票1'
    schema.fromDate = datetime.today()
    schema.toDate = datetime.today()
    schema.createDate = datetime.today()
    schema.creator = 'htx'
    schema.items = [item]

    # assert isinstance(Vote_schema.query, query)
    # aa = Vote_schema.query.all()

    db.session.add(schema)
    db.session.commit()
    pass