#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
# NightOwl - who tests your unit tests?
#
# Copyright (C) 2012 DResearch Fahrzeugelektronik GmbH
# Written and maintained by Erik Bernoth <bernoth@dresearch-fe.de>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version
# 2 of the License, or (at your option) any later version.
#

import unittest
import sys
import os
import inspect

#enable imports from dir above
sys.path.append(os.path.abspath(
    os.path.dirname(inspect.getfile(inspect.currentframe()))+"/.."))

import framework as fw

class TestSignalAccumulator(unittest.TestCase):
    """
    does the testing for framework.SignalAccumulator
    """

    ASSERT_TXT = "expected '{}' \nbut got '{}'"

    def test_add_simple(self):
        #prepare
        expected_count = 1
        attempt=1
        input_ = fw.Signal(1,attempt=attempt)
        #exec
        sut = fw.SignalAccumulator(attempt=attempt,signals=input_)
        #assert
        self.assertEqual(expected_count,sut.count,
                self.ASSERT_TXT.format(expected_count,sut.count))


    def test_add_more(self):
        #prepare
        expected_count = 3
        attempt=1
        input_ = [fw.Signal(i,attempt=attempt) for i in range(expected_count)]
        #exec
        sut = fw.SignalAccumulator(attempt=attempt,signals=input_)
        #assert
        self.assertEqual(expected_count,sut.count,
                self.ASSERT_TXT.format(expected_count,sut.count))


    def test_add_ignore_malformed(self):
        #prepare
        expected_count = 0
        attempt=1
        dont_match=12
        input_ = fw.Signal(attempt=attempt)
        #exec
        sut = fw.SignalAccumulator(attempt=dont_match,signals=input_)
        #assert
        self.assertEqual(expected_count,sut.count,
                self.ASSERT_TXT.format(expected_count,sut.count))


if __name__ == '__main__':
    unittest.main()
