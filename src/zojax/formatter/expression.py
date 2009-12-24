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
""" ``formatter`` TALES expression
Author: Nikolay Kim <fafhrd91@gmail.com>

$Id$
"""
from zope.component import queryAdapter
from zope.proxy import removeAllProxies
from zope.tales.expressions import PathExpr, simpleTraverse

from interfaces import IFormatterFactory
from interfaces import FormatterNotDefined, FormatterExpressionError


class FormatterExpression(PathExpr):
    """ formatter sytax:
       formatter:<formatterName>,<formatterVar1>,<formatterVar2>,...:pathExpr """

    def __init__(self, name, expr, engine, traverser=simpleTraverse):
        parts = expr.split(':', 1)
        try:
            formatterName, pathExpr = parts[0], parts[1]
        except IndexError:
            raise FormatterExpressionError(expr)

        args = formatterName.split(',')
        self.formatterName = args[0]
        self.formatterArgs = args[1:]

        super(FormatterExpression, self).__init__(
            name, pathExpr, engine, traverser=simpleTraverse)

    def __call__(self, econtext):
        request = removeAllProxies(econtext.request)

        factory = queryAdapter(
            request, IFormatterFactory, name=self.formatterName)

        if factory is None:
            raise FormatterNotDefined(self.formatterName)

        formatter = factory(*self.formatterArgs)

        value = super(FormatterExpression, self).__call__(econtext)
        return formatter.format(value)
