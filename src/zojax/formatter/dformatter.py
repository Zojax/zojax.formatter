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
""" ``date`` formatter implementation
Author: Nikolay Kim <fafhrd91@gmail.com>

$Id$
"""
from datetime import date
from simplejson import dumps
from zope import interface, component
from zope.component import getUtility
from zope.publisher.interfaces.http import IHTTPRequest

from zojax.resourcepackage.library import includeInplaceSource

from interfaces import IFormatter, IFormatterFactory, IFormatterConfiglet


jssource = """<script type="text/javascript">
var date_formats = %s;
var month_names = %s;
var day_names = %s;
</script>"""


class DateFormatter(object):
    interface.implements(IFormatter)

    def __init__(self, request, *args):
        try:
            self.tp = args[0]
        except:
            self.tp = 'medium'
        locale = request.locale
        gregorian = locale.dates.calendars.get('gregorian')
        month_names = gregorian.getMonthNames()
        day_names = gregorian.getDayNames()
        formats = map(lambda x: (x, locale.dates.getFormatter('date', x).getPattern()), ['short', 
                                                                                  'medium',
                                                                                  'long',
                                                                                  'full'])
        includeInplaceSource(jssource%(dumps(dict(formats)), \
                                       dumps(month_names), dumps(day_names)))

    def format(self, value):
        if not isinstance(value, date):
            return value

        configlet = getUtility(IFormatterConfiglet)
        formatted = value.strftime(str(getattr(configlet, 'date_'+self.tp)))
    
        return u'<span class="zojax-formatter-date" value="%s" format="%s">%s</span>' \
                % (value.strftime('%B %d, %Y %H:%M:%S %z'), self.tp, formatted)


class DateFormatterFactory(object):
    component.adapts(IHTTPRequest)
    interface.implements(IFormatterFactory)

    def __init__(self, request):
        self.request = request

    def __call__(self, *args, **kw):
        return DateFormatter(self.request, *args)
