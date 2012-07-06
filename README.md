NightOwl - Who tests the unittests?
===================================

![logo.png](/erikb85/master-thesis/raw/logo-1/planning/logo.png)

`NightOwl` is the wise, selfless guard, that will build, test, deploy and
analyse your software on your embedded target.

At the moment it allows you to filter your warnings and errors from your
`bitbake` outputs (or logs) and generate a graph over Error- and Warning-
development over the last builds. Further development is planned, of course,
in form of a Master's thesis. Finally `NightOwl` should be as powerful in
managing your project's development as
[phpUnderControl|phpundercontrol/phpUnderControl].

Installation
------------

To get started you need: Linux, Python2.7, matplotlib and a shell.


Getting Started
---------------

If all requirements are fullfilled you can get started. There is a tutorial
planned for the future. For now you have to use the source code documentation
if you have questions.

Examples:

  1. get errorlogs from your bitbake logs

Code:

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

Code:

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

Code:

    $ bitbake MLO | ./log_errors.py testBuild 3 >>error.log
    $ cat error.log | ./error_to_json.py | grep count | ./graph.py build-error Show-Errors

![build-error.png](opencontrol/raw/master/data/build-error.png)

Further Plans
-------------

green = tool
blue = data files and formats
![structure.png](/erikb85/master-thesis/raw/struct-1/planning/system-structure.png)
