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
from __future__ import print_function

import unittest
import sys
import os
import inspect
#enable importing from one path up
sys.path.append(os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))+'/..')

import json

from to_json import make_notification, make_count, parse_line,parse_errorlog
from constants import *



class TestToJson(unittest.TestCase):

    def test_makeNotification_empty_empty(self):
        #init
        job_name = None
        build_num = None
        notif_type = None
        task_name = None
        message = None
        notif_expect = {'job':job_name,'build':build_num,'type':notif_type,'task':task_name,'message':message}
        #exec
        notif_out = make_notification(job_name,build_num,notif_type,task_name,message)
        #eval
        self.assertEqual(notif_out,notif_expect,
                "'{0}'!='{1}'".format(notif_out,notif_expect))

    def test_makeNotification_simple_same(self):
        #init
        job_name = "testjob"
        build_num = 134
        notif_type = TYPE_ERROR
        task_name = "testtask"
        message = "testmessage abc"
        notif_expect = {'job':job_name,'build':build_num,'type':notif_type,'task':task_name,'message':message}
        #exec
        notif_out = make_notification(job_name,build_num,notif_type,task_name,message)
        #eval
        self.assertEqual(notif_out,notif_expect,
                "'{0}'!='{1}'".format(notif_out,notif_expect))

    def test_makeCount_empty_empty(self):
        #init
        job_name = None
        build_num = None
        notif_type = None
        count = None
        notif_expect = {'job':job_name,'build':build_num,'type':notif_type,'count':count}
        #exec
        notif_out = make_count(job_name,build_num,notif_type,count)
        #eval
        self.assertEqual(notif_out,notif_expect,
                "'{0}'!='{1}'".format(notif_out,notif_expect))

    def test_makeCount_simple_same(self):
        #init
        job_name = "testJob"
        build_num = 321
        notif_type = TYPE_WARNING
        count = 23
        notif_expect = {'job':job_name,'build':build_num,'type':notif_type,'count':count}
        #exec
        notif_out = make_count(job_name,build_num,notif_type,count)
        #eval
        self.assertEqual(notif_out,notif_expect,
                "'{0}'!='{1}'".format(notif_out,notif_expect))

    def test_parseLine_empty_empty(self):
        #init
        txt = ""
        job_name = ""
        build_num = 0
        task_name = ""
        out_expect = ""
        #exec
        out = parse_line(txt,job_name,build_num,task_name)
        #eval
        self.assertEqual(out,out_expect,
                "'{0}'!='{1}'".format(out,out_expect))

    def test_parseLine_warning_notificationWithWarntype(self):
        #init
        txt = "WARNING: this is a test warning"
        job_name = "testJob"
        build_num = 1
        task_name = "testTask"
        out_expect = '{"build": 1, "job": "testJob", "message": "this is a test warning", "task": "testTask", "type": "WARNING"}'
        #exec
        out = parse_line(txt,job_name,build_num,task_name)
        #eval
        self.assertEqual(out,out_expect,
                "'{0}'!='{1}'".format(out,out_expect))

    def test_parseLine_error_notificationWithErrortype(self):
        #init
        txt = "ERROR: this is a test error"
        job_name = "testJob"
        build_num = 1
        task_name = "testTask"
        out_expect = '{"build": 1, "job": "testJob", "message": "this is a test error", "task": "testTask", "type": "ERROR"}'
        #exec
        out = parse_line(txt,job_name,build_num,task_name)
        #eval
        self.assertEqual(out,out_expect,
                "'{0}'!='{1}'".format(out,out_expect))

    def test_parseLine_count_notificationWithCounttype(self):
        #init
        txt = "Error count: 3"
        job_name = "testJob"
        build_num = 1
        task_name = "doesn't matter"
        out_expect = '{"build": 1, "count": 3, "job": "testJob", "type": "ERR_COUNT"}'
        #exec
        out = parse_line(txt,job_name,build_num,task_name)
        #eval
        self.assertEqual(out,out_expect,
                "'{0}'!='{1}'".format(out,out_expect))

    def test_parseErrorlog_empty_empty(self):
        #init
        job_name = None
        build_num = None
        task_name = None
        txt_expect = None
        instream = []
        printed = []
        mock = lambda *args, **kwargs: printed.append(args[0])
        #exec
        parse_errorlog(instream,job_name,build_num,task_name,mprint=mock)
        #eval
        self.assertEqual(len(printed),0,
                "'{0}'!='{1}'".format(len(printed),0))

    def test_parseErrorlog_startEnd_empty(self):
        #init
        job_name = "Testjob"
        build_num = 123
        task_name = "Testtask"
        txt_expect = ""
        instream = [
                "----------[START:{0}({1})]----------".format(job_name,build_num),
                "----------[END:{0}({1})]----------".format(job_name,build_num)
        ]
        printed = []
        mock = lambda *args, **kwargs: printed.append(args[0])
        #exec
        parse_errorlog(instream,job_name,build_num,task_name,mprint=mock)
        #eval
        self.assertEqual(len(printed),0,
                "'{0}'!='{1}'".format(len(printed),0))

    def test_parseErrorlog_complex_complex(self):
        #init
        job_name = None
        build_num = None
        task_name = None
        jobname_expect = "Testjob"
        buildnum_expect = 123
        msg1_expect = "testtext 1 abc"
        msg2_expect = "testtext 2 def"
        task2_expect = "testtask"
        warncount_expect = 1
        errcount_expect = 1
        output_expect = [
                json.dumps(make_notification(jobname_expect,buildnum_expect,TYPE_WARNING,TASK_START,msg1_expect),sort_keys=True),
                json.dumps(make_notification(jobname_expect,buildnum_expect,TYPE_ERROR,task2_expect,msg2_expect),sort_keys=True),
                json.dumps(make_count(jobname_expect,buildnum_expect,TYPE_WARN_COUNT,warncount_expect),sort_keys=True),
                json.dumps(make_count(jobname_expect,buildnum_expect,TYPE_ERROR_COUNT,errcount_expect),sort_keys=True)
        ]
        instream = [
                "----------[START:{0}({1})]----------".format(jobname_expect,buildnum_expect),
                "",
                "[{0}]".format(TASK_START),
                "WARNING: {0}".format(msg1_expect),
                "[{0}]".format(task2_expect),
                "ERROR: {0}".format(msg2_expect),
                "",
                "Warning count: {0}".format(warncount_expect),
                "Error count: {0}".format(errcount_expect),
                "----------[END:{0}({1})]----------".format(jobname_expect,buildnum_expect)
        ]
        printed = []
        mock = lambda *args, **kwargs: printed.append(args[0])
        #exec
        parse_errorlog(instream,job_name,build_num,task_name,mprint=mock)
        #eval
        self.assertEqual(printed,output_expect,
                "'{0}'!='{1}'".format(printed,output_expect))

        def suite():
            suite = unittest.TestLoader().loadTestsFromTestCase(TestToJson)

if __name__ == "__main__":
    unittest.main()
