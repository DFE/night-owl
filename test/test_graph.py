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

class TestGraph(unittest.TestCase):
    """
    does the testing for framework.SignalAccumulator
    """

    ASSERT_TXT = "expected '{}' \nbut got '{}'"

    def test_simple_empty_accumulators(self):
        #prepare
        exp_name = "Testname"
        exp_xlabel = "xlabel"
        exp_ylabel = "ylabel"
        exp_formatting = "no formatting, who needs that anyway"
        exp_xdata = np.array([])
        exp_ydata = np.array([])
        expected = "Graph('{}','{}','{}','{}',{},{})".format(
                exp_name,
                exp_xlabel,
                exp_ylabel,
                exp_formatting,
                exp_xdata,
                exp_ydata
        )
        #execute
        sut = fw.Graph(
                name=exp_name,
                xlabel=exp_xlabel,
                ylabel=exp_ylabel,
                format_=exp_formatting
        )
        #assert
        self.assertEqual(expected,str(sut),
                self.ASSERT_TXT.format(expected,str(sut)))




    def test_apply_accumulators(self):
        """
        tests the depency between the signal_accumulators list and
        the [xy]data variables which are generated with
        the :py:method:framework.Graph.__apply_accumulators().
        """
        #prepare
        expected_data = [3,4,5,6,5]
        signals = [fw.Signal(attempt=attempt) 
                    for attempt, i in enumerate(expected_data)
                    for x in range(i)]
        sut = fw.Graph()
        #exec
        sut.add_signals(signals)
        #assert
        result = [0 for x in expected_data]
        for i,x in enumerate(sut.x_data):
            result[int(x)] = int(sut.y_data[i])
        self.assertEqual(expected_data,result,
                self.ASSERT_TXT.format(expected_data, result))



if __name__ == '__main__':
    unittest.main()
