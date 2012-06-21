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

#enable importing from one path up
sys.path.append(os.getcwd()+'/..')

from filter_errorlog import parse_line, parse_build
from constants import *

class TestFilterErrorlog(unittest.TestCase):

    def test_parseLine_empty_noChanges(self):
        #init
        line = ""
        task, task_printed, warning_count, error_count = START_STATE_ERRORLOGGER
        txt_expect = ""
        type_expect = TYPE_IGNORED
        #exec
        txt_after, type_after = parse_line(line)
        #eval
        self.assertEqual(txt_after,txt_expect,
                "'{0}'!='{1}'".format(txt_after,txt_expect))
        self.assertEqual(type_after,type_expect,
                "'{0}'!='{1}'".format(type_after,type_expect))

    def test_parseLine_Noteline_newTaskname(self):
        #init
        line = "NOTE: package test: Started"
        task, task_printed, warning_count, error_count = START_STATE_ERRORLOGGER
        txt_expect = "[test]"
        type_expect = TYPE_NOTE
        #exec
        txt_after, type_after = parse_line(line)
        #eval
        self.assertEqual(txt_after,txt_expect,
                "'{0}'!='{1}'".format(txt_after,txt_expect))
        self.assertEqual(type_after,type_expect,
                "'{0}'!='{1}'".format(type_after,type_expect))

    def test_parseLine_warning_newOutput(self):
        #init
        line = "waRNiNG: abcdefg hijkl"
        task, task_printed, warning_count, error_count = START_STATE_ERRORLOGGER
        txt_expect = "WARNING: abcdefg hijkl"
        type_expect = TYPE_WARNING
        #exec
        txt_after, type_after = parse_line(line)
        #eval
        self.assertEqual(txt_after,txt_expect,
                "'{0}'!='{1}'".format(txt_after,txt_expect))
        self.assertEqual(type_after,type_expect,
                "'{0}'!='{1}'".format(type_after,type_expect))

    def test_parseLine_error_newOutput(self):
        #init
        line = "eRrOr: abcdefg hijkl"
        task, task_printed, warning_count, error_count = START_STATE_ERRORLOGGER
        txt_expect = "ERROR: abcdefg hijkl"
        type_expect = TYPE_ERROR
        #exec
        txt_after, type_after = parse_line(line)
        #eval
        self.assertEqual(txt_after,txt_expect,
                "'{0}'!='{1}'".format(txt_after,txt_expect))
        self.assertEqual(type_after,type_expect,
                "'{0}'!='{1}'".format(type_after,type_expect))

    def test_parseBuild_empty_logstructureOnly(self):
        #init
        job = "Testjob"
        build = 123
        instream = []
        start_state = None
        out_expect = """\
----------[START:{0}({1})]----------


Warning count: 0
Error count: 0
----------[END:{0}({1})]----------""".format(job,build)
        #exec
        out = parse_build(job,build,instream,start_state)
        #eval
        self.assertEqual(out,out_expect,
                "'{0}'!='{1}'".format(out,out_expect))

    def test_parseBuild_warning_showWarnline(self):
        #init
        job = "Testjob"
        build = 123
        instream = ['warning: abc def']
        start_state = None
        out_expect = """\
----------[START:{0}({1})]----------

[ONSTART]
WARNING: abc def


Warning count: 1
Error count: 0
----------[END:{0}({1})]----------""".format(job,build)
        #exec
        out = parse_build(job,build,instream,start_state)
        #eval
        self.assertEqual(out,out_expect,
                "'{0}'!='{1}'".format(out,out_expect))


    def test_parsebuild_error_showErrorline(self):
        #init
        job = "Testjob"
        build = 123
        instream = ['error: abc def']
        start_state = None
        out_expect = """\
----------[START:{0}({1})]----------

[ONSTART]
ERROR: abc def


Warning count: 0
Error count: 1
----------[END:{0}({1})]----------""".format(job,build)
        #exec
        out = parse_build(job,build,instream,start_state)
        #eval
        self.assertEqual(out,out_expect,
                "'{0}'!='{1}'".format(out,out_expect))

    def test_parseBuild_package_stillEmpty(self):
        #init
        job = "Testjob"
        build = 123
        instream = ['NOTE: package Testpackage: Started']
        start_state = None
        out_expect = """\
----------[START:{0}({1})]----------


Warning count: 0
Error count: 0
----------[END:{0}({1})]----------""".format(job,build)
        #exec
        out = parse_build(job,build,instream,start_state)
        #eval
        self.assertEqual(out,out_expect,
                "'{0}'!='{1}'".format(out,out_expect))

    def test_parseBuild_packageError_showBothlines(self):
        #init
        job = "Testjob"
        build = 123
        instream = ['NOTE: package Testpackage: Started','error: abc def']
        start_state = None
        out_expect = """\
----------[START:{0}({1})]----------

[Testpackage]
ERROR: abc def


Warning count: 0
Error count: 1
----------[END:{0}({1})]----------""".format(job,build)
        #exec
        out = parse_build(job,build,instream,start_state)
        #eval
        self.assertEqual(out,out_expect,
                "'{0}'!='{1}'".format(out,out_expect))

    def test_parseBuild_packageErrorPackage_stillTwolines(self):
        #init
        job = "Testjob"
        build = 123
        instream = ['NOTE: package Testpackage: Started','error: abc def','NOTE: package Invisible: Started']
        start_state = None
        out_expect = """\
----------[START:{0}({1})]----------

[Testpackage]
ERROR: abc def


Warning count: 0
Error count: 1
----------[END:{0}({1})]----------""".format(job,build)
        #exec
        out = parse_build(job,build,instream,start_state)
        #eval
        self.assertEqual(out,out_expect,
                "'{0}'!='{1}'".format(out,out_expect))

    def test_parseBuild_complex_complex(self):
        #init
        job = "Testjob"
        build = 123
        instream = [
            'NOTE: package Testpackage: Started',
            'error: abc def',
            'NOTE: package Testpackage2: Started',
            'warNING: def ghi',
            'ERRoR: qwer ty',
            'ERROr: qwer tz',
            'NOTE: package Invisible: Started'
        ]
        start_state = None
        out_expect = """\
----------[START:{0}({1})]----------

[Testpackage]
ERROR: abc def

[Testpackage2]
WARNING: def ghi
ERROR: qwer ty
ERROR: qwer tz


Warning count: 1
Error count: 3
----------[END:{0}({1})]----------""".format(job,build)
        #exec
        out = parse_build(job,build,instream,start_state)
        #eval
        self.assertEqual(out,out_expect,
                "'{0}'!='{1}'".format(out,out_expect))

if __name__ == "__main__":
    unittest.main()
