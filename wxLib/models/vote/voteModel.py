# -*- encoding: utf-8 -*-
'''
Created on '2014/12/2'

@author: 'hu'
'''

from wxLib.meta.vote.voteMeta import *

if __name__ == '__main__':
    item = Vote_item(itemtitle='item1', itemdesc='item1')
    schema = Vote_schema(schemaname='test1', desc="test1", fromDate=db.DateTime(), toDate=db.DateTime(),
                         createDate=db.DateTime(), creator='htx', items=[item])
    assert isinstance(Vote_schema.query, query)
    aa = Vote_schema.query.all()

    # db.session.add(schema)
    # db.session.commit()
    pass