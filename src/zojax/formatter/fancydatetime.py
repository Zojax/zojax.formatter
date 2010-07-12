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

from pytz import utc, timezone, FixedOffset
from datetime import datetime, timedelta
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
            value = utc.localize(value)

        print value

        value = value.astimezone(tz)

        offset = value.tzinfo.utcoffset(value)
        if offset < timedelta():
            ind = -1
        else:
            ind = 1
        offset = ind*(abs(offset).seconds/600)*10

        value = FixedOffset(offset).normalize(value)

        fdate = unicode(value.strftime(str(getattr(configlet,'date_'+self.tp))))
        ftime = unicode(value.strftime(str(getattr(configlet,'time_'+self.tp))))

        formatted = value.strftime('%B %d, %Y %H:%M:%S %z')

        return u'<span class="zojax-formatter-fancydatetime" date="%s" time="%s" offset="%s" value="%s">%s</span>' \
            % (fdate, ftime, offset, value.strftime('%B %d, %Y %H:%M:%S %z'), formatted)



class FancyDatetimeFormatterFactory(object):
    component.adapts(IHTTPRequest)
    interface.implements(IFormatterFactory)

    def __init__(self, request):
        self.request = request

    def __call__(self, *args, **kw):
        return FancyDatetimeFormatter(self.request, *args)
