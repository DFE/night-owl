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

import numpy as np
import framework as fw

class TestDiagram(unittest.TestCase):
    """
    does the testing for :py:class:framework.Diagram
    TODO add more tests and remove framework depency from Diagram.draw()
    """

    ASSERT_TXT = "expected '{}' \nbut got '{}'"

    def test_simple(self):
        #prepare
        in_filename = "TestFilename"
        in_title = "TestTitle"
        in_all_graphs = []
        expected = "Diagram('{}','{}',{})".format(
                in_filename,
                in_title,
                in_all_graphs
        )
        #exec
        sut = fw.Diagram(in_filename, in_title, in_all_graphs)
        #assert
        self.assertEqual(expected,str(sut),
                self.ASSERT_TXT.format(expected,str(sut)))



if __name__ == '__main__':
    unittest.main()
