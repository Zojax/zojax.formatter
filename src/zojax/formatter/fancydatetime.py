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
""" ``fancyDatetime`` formatter implementation

$Id$
"""

from pytz import utc, timezone
from datetime import datetime
from zope import interface, component
from zope.i18n import translate
from zope.component import getUtility
from zope.publisher.interfaces.http import IHTTPRequest

from interfaces import IFormatter, IFormatterFactory, IFormatterConfiglet


class FancyDatetimeFormatter(object):
    interface.implements(IFormatter)

    def __init__(self, request, *args):
        try:
            self.tp = args[0]
        except:
            self.tp = 'medium'

        self.request = request
        self.formatter = request.locale.dates.getFormatter('dateTime', self.tp)

    def format(self, value):
        if not isinstance(value, datetime):
            return value

        configlet = getUtility(IFormatterConfiglet)

        tz = timezone(configlet.timezone)

        if value.tzinfo is None:
            value = datetime(value.year, value.month, value.day, value.hour,
                             value.minute, value.second, value.microsecond, tz)

        value = value.astimezone(tz)

        fdate = unicode(value.strftime(str(getattr(configlet,'date_'+self.tp))))
        ftime = unicode(value.strftime(str(getattr(configlet,'time_'+self.tp))))
 
        return u'<span class="zojax-formatter-fancydatetime" date="%s" time="%s">%s</span>' \
            % (fdate, ftime, value.strftime('%B %d, %Y %H:%M:%S %z'))



class FancyDatetimeFormatterFactory(object):
    component.adapts(IHTTPRequest)
    interface.implements(IFormatterFactory)

    def __init__(self, request):
        self.request = request

    def __call__(self, *args, **kw):
        return FancyDatetimeFormatter(self.request, *args)
