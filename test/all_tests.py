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
from test_signal import TestSignal
from test_signal_accumulator import TestSignalAccumulator
from test_graph import TestGraph
from test_diagram import TestDiagram

class AllTests(unittest.TestSuite):

    def __init__(self):
        self.addTest(Signal().suite())
        self.addTest(SignalAccumulator().suite())
        self.addTest(Graph().suite())
        self.addTest(Diagram().suite())


if __name__ == "__main__":
	unittest.main()
