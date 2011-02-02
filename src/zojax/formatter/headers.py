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

from zojax.resourcepackage.library import includeInplaceSource


jssource = """<script type="text/javascript">
var datetime_formats = %s;
var time_formats = %s;
var date_formats = %s;
var month_names = %s;
var day_names = %s;
</script>"""


class FormatterHeaders(object):
    

    def update(self):
        super(FormatterHeaders, self).update()
        locale = self.request.locale
        dt_formats = map(lambda x: (x, locale.dates.getFormatter('dateTime', x).getPattern()), ['short', 
                                                                                  'medium',
                                                                                  'long',
                                                                                  'full'])
        
        gregorian = locale.dates.calendars.get('gregorian')
        month_names = gregorian.getMonthNames()
        day_names = gregorian.getDayNames()
        d_formats = map(lambda x: (x, locale.dates.getFormatter('date', x).getPattern()), ['short', 
                                                                                  'medium',
                                                                                  'long',
                                                                                  'full'])
        t_formats = map(lambda x: (x, locale.dates.getFormatter('time', x).getPattern()), ['short', 
                                                                                  'medium',
                                                                                  'long',
                                                                                  'full'])
        
        includeInplaceSource(jssource%(dumps(dict(dt_formats)), \
                                       dumps(dict(t_formats)), \
                                       dumps(dict(d_formats)), \
                                       dumps(month_names), 
                                       dumps(day_names)
                                       ))
    
    def render(self):
        return u''