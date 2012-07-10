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
#enable importing from one path up
sys.path.append(os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))+'/..')

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
        warn_expect = 0
        err_expect = 0
        print_expect = [
            "----------[START:{0}({1})]----------".format(job,build),
            "",
            "",
            "Warning count: {0}".format(warn_expect),
            "Error count: {0}".format(err_expect),
            "",
            "----------[END:{0}({1})]----------""".format(job,build)
        ]
        printed = []
        mock = lambda *args, **kwargs: printed.append(args[0] if len(args)>0 else "")
        #exec
        parse_build(job,build,instream,start_state,mprint=mock)
        #eval
        self.assertEqual(printed,print_expect,
                "'{0}'!='{1}'".format(printed,print_expect))

    def test_parseBuild_warning_showWarnline(self):
        #init
        job = "Testjob"
        build = 123
        instream = ['warning: abc def']
        start_state = None
        warn_expect = 1
        err_expect = 0
        print_expect = [
            "----------[START:{0}({1})]----------".format(job,build),
            "",
            "[{0}]".format(TASK_START),
            "WARNING: abc def",
            "",
            "",
            "Warning count: {0}".format(warn_expect),
            "Error count: {0}".format(err_expect),
            "",
            "----------[END:{0}({1})]----------""".format(job,build)
        ]
        printed = []
        mock = lambda *args, **kwargs: printed.append(args[0] if len(args)>0 else "")
        #exec
        parse_build(job,build,instream,start_state,mprint=mock)
        #eval
        self.assertEqual(printed,print_expect,
                "'{0}'!='{1}'".format(printed,print_expect))

    def test_parsebuild_error_showErrorline(self):
        #init
        job = "Testjob"
        build = 123
        instream = ['error: abc def']
        start_state = None
        warn_expect = 0
        err_expect = 1
        print_expect = [
            "----------[START:{0}({1})]----------".format(job,build),
            "",
            "[{0}]".format(TASK_START),
            "ERROR: abc def",
            "",
            "",
            "Warning count: {0}".format(warn_expect),
            "Error count: {0}".format(err_expect),
            "",
            "----------[END:{0}({1})]----------""".format(job,build)
        ]
        printed = []
        mock = lambda *args, **kwargs: printed.append(args[0] if len(args)>0 else "")
        #exec
        parse_build(job,build,instream,start_state,mprint=mock)
        #eval
        self.assertEqual(printed,print_expect,
                "'{0}'!='{1}'".format(printed,print_expect))

    def test_parseBuild_package_stillEmpty(self):
        #init
        job = "Testjob"
        build = 123
        instream = ['NOTE: package Testpackage: Started']
        start_state = None
        warn_expect = 0
        err_expect = 0
        print_expect = [
            "----------[START:{0}({1})]----------".format(job,build),
            "",
            "",
            "Warning count: {0}".format(warn_expect),
            "Error count: {0}".format(err_expect),
            "",
            "----------[END:{0}({1})]----------""".format(job,build)
        ]
        printed = []
        mock = lambda *args, **kwargs: printed.append(args[0] if len(args)>0 else "")
        #exec
        parse_build(job,build,instream,start_state,mprint=mock)
        #eval
        self.assertEqual(printed,print_expect,
                "'{0}'!='{1}'".format(printed,print_expect))

    def test_parseBuild_packageErrorPackage_stillTwolines(self):
            #init
        job = "Testjob"
        build = 123
        instream = ['NOTE: package Testpackage: Started','error: abc def','NOTE: package Invisible: Started']
        start_state = None
        warn_expect = 0
        err_expect = 1
        print_expect = [
            "----------[START:{0}({1})]----------".format(job,build),
            "",
            "[{0}]".format("Testpackage"),
            "ERROR: abc def",
            "",
            "",
            "Warning count: {0}".format(warn_expect),
            "Error count: {0}".format(err_expect),
            "",
            "----------[END:{0}({1})]----------""".format(job,build)
        ]
        printed = []
        mock = lambda *args, **kwargs: printed.append(args[0] if len(args)>0 else "")
        #exec
        parse_build(job,build,instream,start_state,mprint=mock)
        #eval
        self.assertEqual(printed,print_expect,
                "'{0}'!='{1}'".format(printed,print_expect))

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
        warn_expect = 1
        err_expect = 3
        print_expect = [
            "----------[START:{0}({1})]----------".format(job,build),
            "",
            "[{0}]".format("Testpackage"),
            "ERROR: abc def",
            "",
            "[{0}]".format("Testpackage2"),
            "WARNING: def ghi",
            "ERROR: qwer ty",
            "ERROR: qwer tz",
            "",
            "",
            "Warning count: {0}".format(warn_expect),
            "Error count: {0}".format(err_expect),
            "",
            "----------[END:{0}({1})]----------""".format(job,build)
        ]
        printed = []
        mock = lambda *args, **kwargs: printed.append(args[0] if len(args)>0 else "")
        #exec
        parse_build(job,build,instream,start_state,mprint=mock)
        #eval
        self.assertEqual(printed,print_expect,
                "'{0}'!='{1}'".format(printed,print_expect))

    def suite():
        suite = unittest.TestLoader().loadTestsFromTestCase(TestFilterErrorlog)

if __name__ == "__main__":
    unittest.main()
