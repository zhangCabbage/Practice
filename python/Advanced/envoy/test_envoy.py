#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

class SimpleTest(unittest.TestCase):
    def test_input(self):
        print "test 1"
        self.assertEqual(1==1, True)
        self.assertEqual(1==2, False)

    def test_2(self):
        print "test 2"
        self.assertEqual("zhang", "zhang")

if __name__ == '__main__':
    unittest.main()
