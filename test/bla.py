#!/usr/bin/python2

import inspect
import os
print os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))
