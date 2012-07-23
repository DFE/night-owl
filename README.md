NightOwl - Who tests the unittests?
===================================

![logo.png](/erikb85/master-thesis/raw/logo-1/planning/logo.png)

`NightOwl` is the wise, selfless guard, that will build, test, deploy and
analyse your software on your embedded target.

At the moment it has a small, simple sanity layer that can be easily integrated
into [OpenEmbedded](http://openembedded.org/) via a small script. You can also
put that script into your Jenkins Job, assuming that your Job uses
[OpenEmbedded](http://openembedded.org/) and
[Bitbake](http://bitbake.berlios.de). If you inclode the sanity-run.sh into
your job, you will recieve a specific error-log, which only includes the errors
and warnings, produced by [Bitbake](http://bitbake.berlios.de). Additionally
you will now have a graph, that will track your errors and warnings over the
time of many builds and you can see how things develop over time. In the
following tutorial you will be introduced to a simple way to include everything
into your Jenkins jobs, that you can see the updated results and
errors/warnings in your project page. Stay tuned, there will be more helpful
features in the future!

Getting Started - the Tutorial
------------------------------

The following libraries and tools are needed to follow with this tutorial:

    $ sudo apt-get install git jenkins python2.7 python-numpy python-matplotlib

If you don't use a debian style Linux it should still be possible to find out
how to install these tools on your system, using the tags above after `apt-get
install`.

Now check if everything works correclty. Go to your Terminal and insert the
following commands:

    $ python
    Python 2.7.3 (default, Apr 20 2012, 22:39:59) 
    [GCC 4.6.3] on linux2
    Type "help", "copyright", "credits" or "license" for more information
    >>> import numpy
    >>> import matplotlib.pyplot as plt
    >>> plt.plot([1,2,3],[1,2,3])
    [<matplotlib.lines.Line2D object at 0x2b2d1d0>]
    >>> plt.show()

The first command opens the python shell and shows you the python version. It
should be `2.7.x` with any number as `x`. Then you are in the python shell,
which can be seen by the `>>>` in the beginning of each line. Then you import
as 2 commands the important python libraries. Afterwards you create a small
diagram and show it. You should see something like this:

![plotter.png](/DFE/night-owl/raw/master/data/plotter-screen.png)

If you can't start python, or get another version or don't see a diagram after
`plt.show()` then something is wrong. Try to find out what's wrong and only
continue afterwards.

The next step is to check if Jenkins works correctly. To test that, open a
browser and go to `localhost:8080`. The Jenkins start screen should open.

In the next step you should create a new job according to your needs or use
an existing one. Let the 
[Jenkins Documentation](https://wiki.jenkins-ci.org/display/JENKINS/Use+Jenkins)
help you.

The last prerequesit is to download the night-owl sourcecode. To do that, `cd`
into your shell to the location of your 
[OpenEmbedded](http://openembedded.org/) project. Then write the following:

    $ git clone git://github.com/DFE/night-owl.git

Now you will see that you have created a subfolder, called `night-owl`, with
all the components that you will need to get night-owl to work. Check now, if
the night-owl folder and your OE build folder are on the same level in your
folder hierarchy, that will be important.

Now add to your shell script in your Jenkins job the following line:

    # ... other stuff you are doing in your job script
    /bin/bash -x <night-owl-path>/sanity-run.sh

and replace your `<night-owl-path>`. Then make sure your Jenkins recognises
your archived artifacts (in your Jenkins config in `Post-build Actions` and
add `build/night-owl/night-owl-error.*` to your filters.)

After your next build you should see 2 new artifacts:

  * nightowl-error.log
  * nightowl-error.png

If you don't see them, something went wrong.

In the last step you go to your job's page in Jenkins and add the following
lines to your Job description:

    <b><center><a href="lastSuccessfulBuild/artifact/build/night-owl/nightowl-error.log" >Error Log</a></center></b><br />
    <br />
    <center><img src="lastSuccessfulBuild/artifact/build/night-owl/nightowl-error.png" /></center>

After the artifacts are created you can reload the page and see the diagram of
your job's errors and warnings over time. Of course this diagram will not show
so much interesting stuff after 1 or 2 builds. You have to wait some build
runs until your error.log gets filled up a little.

Last but not least, you can enable auto refresh on your project page. This way
your diagrams get automatically updated in your view.

Script Examples
---------------

here you can see some examples of what you can do with the night-owl scripts
at the moment:

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

![build-error.png](/DFE/night-owl/raw/master/data/build-error.png)

Further Plans
-------------

 * green = tool
 * blue = data files and formats
![structure.png](/erikb85/master-thesis/raw/struct-1/planning/system-structure.png)
