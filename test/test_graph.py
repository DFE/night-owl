#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
# Open Embedded Under Control - the Continuous Integration and Controlling platform for OpenEmbedded Projects
# OEUC error-log - a framework for logging and presentation of errors and warnings
#
# Copyright (C) 2012 DResearch Fahrzeugelektronik GmbH
# Written and maintained by Thilo Fromm <fromm@dresearch-fe.de>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version
# 2 of the License, or (at your option) any later version.
#

import sys
import os
import unittest
import numpy as np
import matplotlib.pyplot as plt

#enable importing from one path up
sys.path.append(os.getcwd()+'/..')

from graph import make_msgline,append_msgline
from constants import *

class TestFilterErrorlog(unittest.TestCase):

    def test_makeMessageline_empty_tuple(self):
        #init
        #exec
        out = make_msgline()
        #eval
        self.assertTrue(isinstance(out,tuple))
        self.assertEqual(len(out),2)
        self.assertTrue(isinstance(out[0],np.ndarray))
        self.assertTrue(isinstance(out[1],np.ndarray))
        self.assertEqual(out[0].size,0)
        self.assertEqual(out[1].size,0)

    def test_makeMessageline_startvalue_tuple(self):
        #init
        #exec
        out = make_msgline(np.array([1]),np.array([2]))
        #eval
        self.assertTrue(isinstance(out,tuple))
        self.assertEqual(len(out),2)
        self.assertTrue(isinstance(out[0],np.ndarray))
        self.assertTrue(isinstance(out[1],np.ndarray))
        self.assertEqual(out[0].size,1)
        self.assertEqual(out[1].size,1)

    def test_appendMsgline_simple_tuplePlusElements(self):
        #init
        sut = make_msgline()
        #exec
        out = append_msgline(sut,3,2)
        #eval
        self.assertTrue(isinstance(out,tuple))
        self.assertEqual(len(out),2)
        self.assertTrue(isinstance(out[0],np.ndarray))
        self.assertTrue(isinstance(out[1],np.ndarray))
        self.assertEqual(out[0].size,1)
        self.assertEqual(out[1].size,1)


if __name__ == "__main__":
	unittest.main()
