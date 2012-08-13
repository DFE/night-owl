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

"""
contains everything related to the user interface for night-owl.
"""

from __future__ import print_function

import framework

class NightOwl(object):
    """
    is the manager class for the night-owl module.
    """

    DEFAULT_FILENAME = "night-owl.png"
    DEFAULT_TITLE = "Night Owl Errors/Warnings"

    def __init__(self):
        pass

    def draw_diagram(self):
        graphs = []
        diagram = Diagram(
            DEFAULT_FILENAME,
            DEFAULT_TITLE,
            graphs
        )
        diagram.draw()
