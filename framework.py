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
manages helper and ORM classes.
"""

import json
import numpy as np

class IgnoredWarning(Warning):
    "is raised, when elements in a sequence are ignored"
    pass


class BadParamException(Exception):
    """is raised, when paramters are given in an incorrect way"""
    pass

class Signal(object):
    """
    is a single message like an error or a warning plus it's additional
    information. 

    At the moment it is just a simple wrapper for the data. Later on, ORM
    functionality should be added.
    """

    TYPE_ERROR = "ERROR"
    TYPE_WARNING = "WARNING"

    def __init__(self,signal_tid=None,type_=None,attempt=None,msg=None,
            cat=None,recipe=None,cmd=None,file_=None,row=None,col=None,
            time=None):
        self.signal_tid = signal_tid if signal_tid >= 0 else -1
        self.type_ = type_ if type_ else ""
        self.attempt = attempt if attempt >= 0 else -1
        self.msg = msg if msg else ""
        self.cat = cat if cat else ""
        self.recipe = recipe if recipe else ""
        self.cmd = cmd if cmd else ""
        self.file_ = file_ if file_ else ""
        self.row = row if row >= 0 else -1
        self.col = col if col >= 0 else -1
        self.time = time if time else ""


    def __str__(self):
        """"""
        #contains a tuple, because it will autoparse to useful string
        return "Signal{}".format((
            self.signal_tid,
            self.type_,
            self.attempt,
            self.msg,
            self.cat,
            self.recipe,
            self.cmd,
            self.file_,
            self.row,
            self.col,
            self.time
        ))


    @classmethod
    def __make_single_from_json(cls,txt):
        """
        is a factory function to parse directly from json

        :param txt: is a :py:class:Signal as a valid json string
        :return: :py:class:Signal object
        """
        json_ = json.loads(txt)
        return Signal(
                json_["signal_tid"],
                json_["type"],
                json_["attempt"],
                json_["msg"],
                json_["cat"],
                json_["recipe"],
                json_["cmd"],
                json_["file"],
                json_["row"],
                json_["col"],
                json_["time"],
        )


    @classmethod
    def make_from_json(cls,input_):
        """
        is a factory function that parses lines of JSON to
        :py:class:framework.Signal objects.

        The idea of reading Iterables and returning generators keeps in mind,
        that this method will likely handle thousands of Signal instances.

        :param input_: an iterable or a single line of JSON text
        :return: a generator that creates Signal objects
        """
        import collections as c
        data = input_ if isinstance(input_,c.Iterable) else (input_,)
        return (cls.__make_single_from_json(txt) for txt in data)



class SignalAccumulator(object):
    """
    maintains a group of signals
    """

    DEFAULT_TYPE = "NO_TYPE"

    def __init__(self, *signals, **kwargs):
        self.type_ = kwargs.pop("type_", self.DEFAULT_TYPE)
        self.attempt = kwargs.pop("attempt",-1)
        self.count = kwargs.pop("count",0)
        self.add_signals(*signals)


    def add_signals(self,*signals):
        for signal in signals:
            if signal.attempt != self.attempt:
                raise IgnoredWarning(("Attempt {} isn't mine ({}) -> " \
                      + "signal ignored").format(signal.attempt, self.attempt))
                continue
            elif signal.type_ != self.type_:
                raise IgnoredWarning(("Type '{}' isn't mine '{}' -> " \
                        + "signal ignored").format(signal.type_, self.type_)
            else:
                self.count +=1


    @classmethod
    def make_many(cls,*signals):
        """
        can be used, when you have a long list of signals of different attempts
        and you want to automatically create a list 
        of :py:class:SignalAccumulator objects for each attempt.

        FIXME: maybe this is all not nessesary anymore, because
        :py:class:framework.Graph has now the responsibility to create
        different :py:class:framework.SignalAccumulator objects?

        :param signal_iterator: should deliver :py:class:signal.Signal objects
        :return: a generator for all :py:class:SignalAccumulator objects
        """
        accumulators = {}
        for signal in signals:
            if signal.attempt not in accumulators:
                accumulators[signal.attempt] = cls(attempt=signal.attempt)
            accumulators[signal.attempt].add_signals(signal)
        #the dict was just a helper, users should just get an iterable
        keys = accumulators.keys()
        keys.sort()
        return (accumulators[k] for k in keys)

    def __str__(self):
        return "SignalAccumulator('{}',{},{})".format(
                self.type_,
                self.attempt,
                self.count
        )



class Graph(object):
    """
    contains all data and information about a single graph inside a
    :py:class:diagram.Diagram.

    Never update the list in signal_accumulators directly. Always reset it.
    Otherwise the follow up data will not be updated and you still generate
    the old graph!
    """

    DEFAULT_NAME="NO_NAME"
    DEFAULT_XLABEL="x-axis"
    DEFAULT_YLABEL="y-axis"
    DEFAULT_FORMATTING="r--"

    def __init__(self, *signal_accumulators, **kwargs):
        """
        :param signal_accumulators: an iterator for signal_accumulators
        :param name: how the graph will be called in the diagram
        :param ylabel: naming of the corresponding y-axis in the diagram
        :param formatting: Matlab style formatting for this graph
        """
        self.__signal_accumulators = signal_accumulators
        self.name = kwargs.pop("name",self.DEFAULT_NAME)
        self.xlabel = kwargs.pop("xlabel",self.DEFAULT_XLABEL)
        self.ylabel = kwargs.pop("ylabel",self.DEFAULT_YLABEL)
        self.formatting = kwargs.pop("formatting",self.DEFAULT_FORMATTING)
        self.__xdata = np.array([])
        self.__ydata = np.array([])
        self.__applied = False


    def __apply_accumulators(self):
        """
        generate pylab parsable data from accumulators
        """
        self.__xdata = np.array([])
        self.__ydata = np.array([])
        for acc in self.signal_accumulators:
            self.__xdata = self.__array_append(self.__xdata,acc.attempt)
            self.__ydata = self.__array_append(self.__ydata,acc.count)
        self.__applied = True


    def __array_append(self, in_a,in_b):
        """
        append a numpy array to another
        :param in_a: a numpy array
        :param in_b: a numpy array or a number
        """
        types = (int,float,long,complex)
        in_b = np.array([in_b]) if isinstance(in_b,types) else in_b
        return np.concatenate((in_a,in_b))


    @property
    def signal_accumulators(self):
        """
        a list of :py:class:signal_accumulator.SignalAccumulator

        please don't update this array, always reset it! Otherwise the follow
        up data will not be updated!
        """
        return self.__signal_accumulators


    @signal_accumulators.setter
    def signal_accumulators(self,*values):
        self.__signal_accumulators = values
        self.__applied = False


    @signal_accumulators.deleter
    def signal_accumulators(self):
        self.__signal_accumulators = None
        self.__xdata = None
        self.__ydata = None
        self.__applied = True


    @property
    def x_data(self):
        """
        generates data for the x values of a pylab graph plot
        """
        if not self.__applied:
            self.__apply_accumulators()
        return self.__xdata


    @property
    def y_data(self):
        """
        generates data for the y values of a pylab graph plot
        """
        if not self.__applied:
            self.__apply_accumulators()
        return self.__ydata


    def __str__(self):
        return "Graph('{}','{}','{}','{}',{},{})".format(
                self.name,
                self.xlabel,
                self.ylabel,
                self.formatting,
                self.x_data,
                self.y_data
        )



class Diagram(object):
    """
    can read json from an input stream and create pylab graphs from it.
    The resulting diagram will be JPEG file containing a title, a named x-axis,
    a named y-axis on the left showing the number of warnings, a named y-axis
    on the right showing the number of errors and 2 graphs, for warnings and
    errors separated.
    """

    DEFAULT_FILENAME="plot.png"
    DEFAULT_TITLE="Diagram"
    DEFAULT_GRAPH_LIST = []


    def __init__(self, filename=None, title=None,all_graphs=None):
        """
        :param filename: is the location, where the graph JPEG should be stored
        :param title: is the graph title that is written above the diagram
        """
        self.filename = filename if filename else self.DEFAULT_FILENAME
        self.title = title if title else self.DEFAULT_TITLE
        self.all_graphs = all_graphs if all_graphs else self.DEFAULT_GRAPH_LIST

    def add_signals(signals):
        """
        TODO: Create a new graph for every new signal type you spot, add a new
              SignalAccumulator to every Graph for every attempt you spot
              and then add the signals to the SignalAccumulators (which maybe
              should be done indirectly through the Graph objects)
        """


    def draw(self):
        """
        draws the graph with help of pylab. All values are taken from
        Object attributes, so there is neither input nor output needed.
        """
        plots = []
        for element in all_graphs:
            if isinstance(element,tuple):
                if len(element) != 2:
                    raise IgnoredWarning("expected a tuple of size 2.\n"\
                            + "More graphs in one diagram isn't meaningful. "\
                            + "Ignored '{}'".format(element))
                    continue
                if not all((isinstance(e,Graph) for e in element)):
                    raise IgnoredWarning("both elements should be element of "\
                            + "Graph. Ignored '{}'".format(element))
                    continue
                both = element # improving readability
                plot1 = plt.figure().add_subplot(111)
                plots.append(plot1)
                self.__init_plot(plot1)
                plot2 = plot1.twinx()
                plots.add(plot2)
                self.__init_plot(plot2)

            elif isinstance(element, Graph):
                single = element #improve readability
                plot = plt.figure().add_subplot(111)
                plots.append(plot)
                self.__init_plot(plot)

            else:
                raise IgnoredWarning("expect ellements to be tuple or Graph,"\
                        + "but found '{}'".format(element))
                continue
        plt.title(self.title)
        plt.savefig(self.filename)
        return self

    def __init_plot(self,plot,graph):
        """
        does some of the repeatable pylab tasks on a plot object, which are
        basically just data transfering tasks from a Graph object to the
        plot object
        """

        plot.set_xlabel(graph.xlabel)
        plot.set_ylabel(graph.ylabel)
        plot.plot(graph.xdata, graph.ydata,graph.formatting,
                label=graph.name)
        plot.axis([0,graph.xdata.max()*1.1,
                    0,graph.ydata.max()*1.1])
        return plot

    def __str__(self):
        return "Diagram('{}','{}',{})".format(
                self.filename,
                self.title,
                self.all_graphs
        )
