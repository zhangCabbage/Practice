#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INT, CHAR, DATETIME, create_engine
from sqlalchemy.orm import sessionmaker

import unittest

def sqlalchemyTest():
    """ 使用sqlalchemy可进行orm操作，也可以直接使用engine或connection """
    print "sqlalchemy version is {}".format(sqlalchemy.__version__)
    Base = declarative_base()
    class Orders(Base):
        """  """
        __tablename__ = 'Orders'

        order_num = Column(INT, primary_key=True)
        order_date = Column(DATETIME)
        cust_id = Column(CHAR)

    engine = create_engine("mysql://root:123456@localhost:3306/SQLearn")
    DBsession = sessionmaker(bind=engine)
    session = DBsession()
    orders = session.query(Orders).all()
    for order in orders:
        print order.order_num, order.order_date, order.cust_id

def unittestTest():
    """  """
    class ModuleTest(unittest.TestCase):
        def firstTest(self):
            print "First Test"
            self.assertEqual(1==2, False)

    unittest.main()

if __name__ == '__main__':
    sqlalchemyTest()
    unittestTest()
