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
""" ``humanDatetime`` formatter implementation

$Id$
"""
from pytz import utc, timezone, FixedOffset
from datetime import datetime, timedelta
from zope import interface, component
from zope.i18n import translate
from zope.component import getUtility
from zope.publisher.interfaces.http import IHTTPRequest

from interfaces import _, IFormatter, IFormatterFactory, IFormatterConfiglet


class HumanDatetimeFormatter(object):
    interface.implements(IFormatter)

    messages = {'past': {'year': u'${value} year(s) ago',
                         'month': u'${value} month(s) ago',
                         'week': u'${value} week(s) ago',
                         'day': u'${value} day(s) ago',
                         'hour': u'${value} hour(s) ago',
                         'minute': u'${value} minute(s) ago',
                         'second': u'${value} second(s) ago',
                         },
                'future': {'year': u'in ${value} year(s)',
                           'month': u'in ${value} month(s)',
                           'week': u'in ${value} week(s)',
                           'day': u'in ${value} day(s)',
                           'hour': u'in ${value} hour(s)',
                           'minute': u'in ${value} minute(s)',
                           'second': u'in ${value} second(s)',
                           }}

    def __init__(self, request, *args):
        self.request = request

    def format(self, value):
        configlet = getUtility(IFormatterConfiglet)

        tz = timezone(configlet.timezone)

        if value.tzinfo is None:
            value = utc.localize(value)

        value = value.astimezone(tz)

        now = datetime.now(utc)
        delta = now - value.astimezone(utc)
        key = 'past'
        if delta < timedelta():
            delta = - delta + timedelta(seconds=1) #due to python implementation
            key = 'future'

        offset = value.tzinfo.utcoffset(value)
        if offset < timedelta():
            ind = -1
        else:
            ind = 1
        offset = ind*(abs(offset).seconds/600)*10

        value = FixedOffset(offset).normalize(value)

        years, months, weeks, hours, minutes = (
            delta.days/365, delta.days/30, delta.days/7,
            delta.seconds/3600, delta.seconds/60)
        formatted = None

        if years > 0:
            formatted = translate(self.messages[key]['year'], 'zojax.formatter',
                                  mapping={'value': years})
        elif months > 0:
            formatted = translate(self.messages[key]['month'],'zojax.formatter',
                                  mapping={'value': months})
        elif weeks > 0:
            formatted = translate(self.messages[key]['week'], 'zojax.formatter',
                                  mapping={'value': weeks})
        elif delta.days > 0:
            formatted = translate(self.messages[key]['day'], 'zojax.formatter',
                                  mapping={'value': delta.days})
        elif hours > 0:
            formatted = translate(self.messages[key]['hour'], 'zojax.formatter',
                                  mapping={'value': hours})
        elif minutes > 0:
            formatted = translate(
                self.messages[key]['minute'], 'zojax.formatter',
                mapping={'value': minutes})
        else:
            formatted = translate(
                self.messages[key]['second'], 'zojax.formatter',
                mapping={'value': delta.seconds})

        return """<span class="zojax-formatter-humandatetime" value="%s">%s</span>""" \
                % (value.strftime('%B %d, %Y %H:%M:%S %z'), formatted)


class HumanDatetimeFormatterFactory(object):
    component.adapts(IHTTPRequest)
    interface.implements(IFormatterFactory)

    def __init__(self, request):
        self.request = request

    def __call__(self, *args, **kw):
        return HumanDatetimeFormatter(self.request, *args)
