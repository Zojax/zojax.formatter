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
""" ``dateTime`` formatter implementation
Author: Nikolay Kim <fafhrd91@gmail.com>

$Id$
"""
from pytz import timezone
from datetime import datetime, timedelta

from zope import interface, component
from zope.component import getUtility
from zope.interface.common.idatetime import ITZInfo
from zope.publisher.interfaces.http import IHTTPRequest

from interfaces import IFormatter, IFormatterFactory, IFormatterConfiglet
from dformatter import DateFormatter


class DatetimeFormatter(DateFormatter):
    interface.implements(IFormatter)

    def format(self, value):
        if not isinstance(value, datetime):
            return value

        configlet = getUtility(IFormatterConfiglet)

        tz = timezone(configlet.timezone)
        if value.tzinfo is None:
            value = datetime(value.year, value.month, value.day, value.hour,
                             value.minute, value.second, value.microsecond, tz)

        value = value.astimezone(tz)
        
        offset = value.tzinfo.utcoffset(value)
        if offset < timedelta():
            ind = -1
        else:
            ind = 1
        offset = ind*(abs(offset).seconds/600)*10

        format = '%s %s'%(
            getattr(configlet, 'date_'+self.tp),
            getattr(configlet, 'time_'+self.tp))
        
        formatted = unicode(value.strftime(str(format)))
        return u'<span class="zojax-formatter-datetime" value="%s" format="%s" offset="%s">%s</span>' \
                % (value.strftime('%B %d, %Y %H:%M:%S %z'), self.tp, offset, formatted)


class DatetimeFormatterFactory(object):
    component.adapts(IHTTPRequest)
    interface.implements(IFormatterFactory)

    def __init__(self, request):
        self.request = request

    def __call__(self, *args, **kw):
        return DatetimeFormatter(self.request, *args)
