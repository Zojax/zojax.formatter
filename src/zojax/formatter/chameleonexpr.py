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
from zope.component import queryAdapter

from chameleon.core import types
from chameleon.zpt import expressions
from z3c.pt.expressions import path_translator

from interfaces import \
    IFormatterFactory, FormatterNotDefined, FormatterExpressionError


class FormatterExpression(object):

    def __call__(self, request, formatterName, formatterArgs, value):
        factory = queryAdapter(
            request, IFormatterFactory, name=formatterName)

        if factory is None:
            raise FormatterNotDefined(self.formatterName)

        return factory(*formatterArgs).format(value)


class FormatterTranslator(expressions.ExpressionTranslator):

    symbol = '_get_zojax_formatter'
    formatter_traverse = FormatterExpression()

    def translate(self, string, escape=None):
        parts = string.strip().split(':', 1)

        try:
            formatterName, string = parts[0], parts[1]
        except IndexError:
            raise SyntaxError(string)

        string = path_translator.translate(string, escape)

        args = formatterName.split(',')
        formatterName = args[0]
        formatterArgs = args[1:]

        value = types.value(
            "%s(request, '%s', %s, %s)" % \
            (self.symbol, formatterName, formatterArgs, string))

        value.symbol_mapping[self.symbol] = self.formatter_traverse

        return value
