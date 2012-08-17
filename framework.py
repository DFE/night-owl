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

    DEFAULT_TID = -1
    DEFAULT_TYP = "NO_TYPE"
    DEFAULT_ATM = -1
    DEFAULT_MSG = ""
    DEFAULT_CAT = ""
    DEFAULT_REC = ""
    DEFAULT_CMD = ""
    DEFAULT_FIL = ""
    DEFAULT_ROW = -1
    DEFAULT_COL = -1
    DEFAULT_TIM = "EMPTY"

    def __init__(self,signal_tid=None,type_=None,attempt=None,msg=None,
            cat=None,recipe=None,cmd=None,file_=None,row=None,col=None,
            time=None):
        self.signal_tid = signal_tid if signal_tid >= 0 else self.DEFAULT_TID
        self.type_ = type_ if type_ is not None else self.DEFAULT_TYP
        self.attempt = attempt if attempt >= 0 else self.DEFAULT_ATM
        self.msg = msg if msg is not None else self.DEFAULT_MSG
        self.cat = cat if cat else self.DEFAULT_CAT
        self.recipe = recipe if recipe else self.DEFAULT_REC
        self.cmd = cmd if cmd else self.DEFAULT_CMD
        self.file_ = file_ if file_ else self.DEFAULT_FIL
        self.row = row if row >= 0 else self.DEFAULT_ROW
        self.col = col if col >= 0 else self.DEFAULT_COL
        self.time = time if time else self.DEFAULT_TIM


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

        :param txt: NO_TYPEpy:class:Signal as a valid json string
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
    maintains a group of signals of the same attempt
    The result is useful for a point of a graph with x being the attempt and
    y being the count, i.e. the number of Signals counted
    """

    DEFAULT_ATTEMPT = -1
    DEFAULT_COUNT = 0
    WARN_MSG = "type_ or attempt didn't match for {} signals"

    def __init__(self, attempt=None, count=None, signals=None):
        self.attempt = attempt if attempt is not None else self.DEFAULT_ATTEMPT
        self.count = count if count is not None else self.DEFAULT_COUNT
        self.add_signals(signals)


    def accept_signal(self,signal):
        return hasattr(signal,'attempt') and self.attempt == signal.attempt

    def add_signals(self,signals):
        """
        adds up signals to the current count. It won't remember the signals
        afterwards. All signals that don#t have an attempt or not the correct
        one are ignored silently.

        TOOD: add logger functionality to allow Messaging of ignored signals
        """
        if signals is None:
            signals = ()
        elif isinstance(signals,Signal):
            #just for not writing the same functionality twice
            signals = (signals,)
        signals = signals if signals is not None else ()
        filtered_sigs = filter(self.accept_signal,signals) 
        self.count += len(filtered_sigs)


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

    DEFAULT_TYPE = Signal.DEFAULT_TYP
    DEFAULT_NAME="NO_NAME"
    DEFAULT_XLABEL="x-axis"
    DEFAULT_YLABEL="y-axis"
    DEFAULT_FORMAT="r--"

    def __init__(self, type_=None, name=None, xlabel=None, ylabel=None,
            format_=None, signals=None):
        """
        :param type_: what Signal.type_ is stored in this graph
        :param name: how the graph will be called in the diagram
        :param xlabel: naming of the corresponding x-axis in the diagram
        :param ylabel: naming of the corresponding y-axis in the diagram
        :param format_: Matlab style formatting for this graph
        :param signals: :py:class:framework.Signal objects to add to that graph
        """
        self.type_ = type_ if type_ is not None else self.DEFAULT_TYPE
        self.name = name if name is not None else self.DEFAULT_NAME
        self.xlabel = xlabel if xlabel is not None else self.DEFAULT_XLABEL
        self.ylabel = ylabel if ylabel is not None else self.DEFAULT_YLABEL
        self.format_ = format_ if format_ is not None else self.DEFAULT_FORMAT
        self.__accumulators = {}
        self.__applied = False


    def __apply_accumulators(self):
        """
        generate pylab parsable data from accumulators
        """
        self.__xdata = np.array([])
        self.__ydata = np.array([])
        for acc in self.__accumulators.values():
            self.__xdata = self.__array_append(self.__xdata,acc.attempt)
            self.__ydata = self.__array_append(self.__ydata,acc.count)
        self.__applied = True


    def __array_append(self, in_a,in_b):
        """
        appends a numpy array to another.
        
        That's basically a helper function to improve the code quality of the
        rest of the class.
        :param in_a: a numpy array
        :param in_b: a numpy array or a number
        """
        types = (int,float,long,complex)
        in_b = np.array([in_b]) if isinstance(in_b,types) else in_b
        return np.concatenate((in_a,in_b))


    def check_signal(self,signal):
        return hasattr(signal,"type_") and signal.type_ == self.type_\
                and hasattr(signal,"attempt")


    def add_signals(self,signals):
        """
        includes signals in this graph. Signals with the wrong type will be
        ignored and signals with different attempts might lead to adding new
        SignalAccumulators internally.

        :param signals: the signals that should be added to this graph
        """
        if signals is None:
            signals = ()
        elif isinstance(signals,Signal):
            signals = (signals,)
        for signal in signals:
            if not self.check_signal(signal):
                continue
            if signal.attempt not in self.__accumulators:
                self.__accumulators[signal.attempt] = SignalAccumulator(
                    attempt=signal.attempt
                )
            self.__accumulators[signal.attempt].add_signals(signal)


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
                self.format_,
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


    def draw(self):
        """
        draws the graph with help of pylab. All values are taken from
        Object attributes, so there is neither input nor output needed.
        """
        plots = []
        for element in all_graphs:
            if isinstance(element,tuple):
                if len(element) != 2:
                    continue
                if not all((isinstance(e,Graph) for e in element)):
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
        self.__write_to_file()


    def __write_to_file(self):
        """
        encapsulates file I/O for improved testability. 
        """
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
