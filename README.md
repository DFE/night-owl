OEUC error-log
==============

OEUC error-log is the power tool for managing errors and warnings in your
OpenEmbedded project. As first part of the OpemEmbeddedUnderControl (OEUC)
platform it helps you in automating your product development process and
gives you a fast and precise overview about the problems your project might
have.

Installation
------------

To get started you need: Python2.7, matplotlib and `/bin/sh`.


Getting Started
---------------

If all requirements are fullfilled you can get started. There is a tutorial
planned for the future. For now you have to use the source code documentation.

Examples:

  1. get errorlogs from your bitbake logs

    $ bitbake myMLO | ./log_errors.py testBuild 1 >error.log
    $ cat error.log
    -------[START:testBuild(1)]-------

    [abc-1.1.1-r123: task do_fetch]
    WARNING: blabla
    ERROR: foo

    [def-1.0.3-r321: task do_build]
    ERROR: oha
    WARNING: bar

    Error count: 2
    Warning count: 2
    -------[END:testBuild(1)]-------

  2. get the same output as json (e.g. to drop it into a database)

    $ bitbake MLO | ./log_errors.py testBuild 2 >>error.log
    $ cat error.log | ./error_to_json.py
    {"build": "1", "job": "myMLO", "message": "blabla", "task": "abc-1.1.1-r123: task do_fetch", "type": "WARNING"}
    {"build": "1", "job": "myMLO", "message": "foo", "task": "abc-1.1.1-r123: task do_fetch", "type": "ERROR"}
    {"build": "1", "job": "myMLO", "message": "oha", "task": "def-1.0.3-r321: task do_build", "type": "ERROR"}
    {"build": "1", "job": "myMLO", "message": "bar", "task": "def-1.0.3-r321: task do_build", "type": "WARNING"}
    {"build": "1", "count": "2", "job": "myMLO", "type": "WARNING"}
    {"build": "1", "count": "2", "job": "myMLO", "type": "ERROR"}
    {"build": "2", "job": "myMLO", "message": "blabla", "task": "abc-1.1.1-r123: task do_fetch", "type": "WARNING"}
    {"build": "2", "job": "myMLO", "message": "foo", "task": "abc-1.1.1-r123: task do_fetch", "type": "ERROR"}
    {"build": "2", "job": "myMLO", "message": "oha", "task": "def-1.0.3-r321: task do_build", "type": "ERROR"}
    {"build": "2", "job": "myMLO", "message": "bar", "task": "def-1.0.3-r321: task do_build", "type": "WARNING"}
    {"build": "2", "count": "2", "job": "myMLO", "type": "WARNING"}
    {"build": "2", "count": "2", "job": "myMLO", "type": "ERROR"}

  3. graph the errors/warnings over builds

    $ bitbake MLO | ./log_errors.py testBuild 3 >>error.log
    $ cat error.log | ./error_to_json.py | grep count | ./graph.py build-error Errors_Graph Build Count

![build-error.png](data/build-error.png)
