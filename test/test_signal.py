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
import json

#enable imports from dir above
sys.path.append(os.path.abspath(
    os.path.dirname(inspect.getfile(inspect.currentframe()))+"/.."))

import framework


class TestSignal(unittest.TestCase):
    """
    does the testing for framework.Signal
    """

    ASSERT_TXT = "expected '{}' \nbut got '{}'"

    def test_from_json(self):
        #prepare
        data = {
            u"signal_tid": 1, 
            u"type": u"ERROR", 
            u"attempt":1,
            u"msg": u"hello Error",
            u"cat": u"NO_CAT",
            u"recipe": u"NO_REC",
            u"cmd": u"do_test",
            u"file": u"/dev/null",
            u"row":0,
            u"col":0,
            u"time": u"2012-09-13 13:41"
        }
        input_ = json.dumps(data)
        expected = str(framework.Signal(
                data["signal_tid"],
                data["type"],
                data["attempt"],
                data["msg"],
                data["cat"],
                data["recipe"],
                data["cmd"],
                data["file"],
                data["row"],
                data["col"],
                data["time"]
        ))
        #execute
        result = str(framework.Signal.make_from_json(input_))
        #assert
        self.assertEqual(expected,result,
                self.ASSERT_TXT.format(expected,result))



if __name__ == '__main__':
    unittest.main()
