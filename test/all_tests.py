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
from test_filter_errorlog import TestFilterErrorlog
from test_graph import TestGraph
from test_to_json import TestToJson

class AllTests(unittest.TestSuite):

    def __init__(self):
        self.addTest(TestFilterErrorlog().suite())
        self.addTest(TestGraph().suite())
        self.addTest(TestToJson().suite())


if __name__ == "__main__":
	unittest.main()
