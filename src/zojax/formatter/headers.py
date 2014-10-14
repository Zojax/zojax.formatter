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

from simplejson import dumps

from zope.component import getUtility

from zojax.resourcepackage.library import includeInplaceSource

from interfaces import IFormatterConfiglet


jssource = """<script type="text/javascript">
var datetime_formats = %s;
var time_formats = %s;
var date_formats = %s;
var month_names = %s;
var day_names = %s;
</script>"""


def replaceTimeFormat(data, format='12'):
    """ replaces the time format """

    if format == '24':
        return map(lambda x: (x[0], x[1].replace('h:mm:ss a', 'H:mm:ss').replace('h:mm a', 'H:mm')), data)
    else:
        return map(lambda x: (x[0], x[1].replace('H:mm:ss', 'h:mm:ss a').replace('H:mm', 'h:mm a')), data)


def returnFormats(dates, formatter):
    """ returns datetime formats """

    return map(lambda x: (x, dates.getFormatter(formatter, x).getPattern()), ['short',
                                                                              'medium',
                                                                              'long',
                                                                              'full'])


class FormatterHeaders(object):

    def update(self):
        super(FormatterHeaders, self).update()

        locale = self.request.locale
        configlet = getUtility(IFormatterConfiglet)
        timeformat = getattr(configlet, 'timeFormat', None)

        dt_formats = returnFormats(locale.dates, 'dateTime')

        gregorian = locale.dates.calendars.get('gregorian')
        month_names = gregorian.getMonthNames()
        day_names = gregorian.getDayNames()

        if gregorian.getDayTypeFromAbbreviation('Mon') == 1:
            day_names.insert(0, day_names[-1])
            del day_names[-1]

        d_formats = returnFormats(locale.dates, 'date')

        t_formats = returnFormats(locale.dates, 'time')

        if timeformat:
            dt_formats = replaceTimeFormat(dt_formats, timeformat)
            t_formats = replaceTimeFormat(t_formats, timeformat)

        includeInplaceSource(jssource % (dumps(dict(dt_formats)),
                                         dumps(dict(t_formats)),
                                         dumps(dict(d_formats)),
                                         dumps(month_names),
                                         dumps(day_names)
                                         ))

    def render(self):
        return u''
