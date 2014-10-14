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
""" zojax.formatter interfaces

$Id$
"""
import vocabulary
from zope import schema, interface
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('zojax.formatter')


class FormatterNotDefined(Exception):
    """ """


class FormatterExpressionError(Exception):
    """ """


class IFormatterConfiglet(interface.Interface):
    """ formatter configlet schema """

    date_short = schema.TextLine(
        title = _(u'Short date format'),
        default = u'%m/%d/%y',
        required = True)

    date_medium = schema.TextLine(
        title = _(u'Medium date format'),
        default = u'%b %d, %Y',
        required = True)

    date_long = schema.TextLine(
        title = _(u'Long date format'),
        default = u'%B %d, %Y',
        required = True)

    date_full = schema.TextLine(
        title = _(u'Full date format'),
        default = u'%A, %B %d, %Y',
        required = True)

    time_short = schema.TextLine(
        title = _(u'Short time format'),
        default = u'%I:%M %p',
        required = True)

    time_medium = schema.TextLine(
        title = _(u'Medium time format'),
        default = u'%I:%M:%S %p',
        required = True)

    time_long = schema.TextLine(
        title = _(u'Long time format'),
        default = u'%I:%M:%S %p %z',
        required = True)

    time_full = schema.TextLine(
        title = _(u'Full time format'),
        default = u'%I:%M:%S %p %Z',
        required = True)

    timezone = schema.Choice(
        title = _(u'Timezone'),
        description = _(u'Portal timezone.'),
        default = 'US/Pacific',
        vocabulary = vocabulary.timezones,
        required = False)

    timeFormat = schema.Choice(
        title = _(u'Time format (12 hours / 24 hours)'),
        values = ['12', '24'],
        default = '12',
        required = False)

    #principalTimezone = schema.Bool(
    #    title = _(u'Use principal timezone'),
    #    description = _(u'Render datetime with user selected timezone.'),
    #    default = True,
    #    required = False)


class IFormatterFactory(interface.Interface):
    """ formatter factory """

    def __call__(*args):
        """ create formatter """


class IFormatter(interface.Interface):
    """ locale formatter """

    def format(value):
        """ format value """


class IStaticFormatter(interface.Interface):
    """ """
