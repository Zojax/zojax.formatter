##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from pytz import timezone
from datetime import datetime
from zope import interface, component
from zope.component import getUtility
from zope.publisher.interfaces.http import IHTTPRequest
from zope.size.interfaces import ISized

from interfaces import IFormatter, IFormatterFactory, IFormatterConfiglet


class NumberFormatter(object):
    interface.implements(IFormatter)

    def __init__(self, request, *args):
        self.tp = args[0]
        try:
            self.length = args[1] and args[1] or None
        except IndexError:
            self.length = None
        try:
            self.name = args[2]
        except IndexError:
            self.name = None
        self.formatter = request.locale.numbers.getFormatter(self.tp, length=self.length, name=self.name)


    def format(self, value):
        return self.formatter.format(value)


class NumberFormatterFactory(object):
    component.adapts(IHTTPRequest)
    interface.implements(IFormatterFactory)

    def __init__(self, request):
        self.request = request

    def __call__(self, *args, **kw):
        return NumberFormatter(self.request, *args)
