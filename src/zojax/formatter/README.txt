===============
zojax.formatter
===============

This package adds extensible tales expression for various formatters.
You can change formatter setting per site basis (zojax.controlpanel).

For configure default settings, add following code to zope.conf

<product-config zojax.formatter>
  timezone UTC
</product-config>

Values for timezoneFormat are:
    1: No timezone

We need register controlpanel configlet

  >>> from zope.configuration import xmlconfig
  >>> context = xmlconfig.string("""
  ... <configure xmlns:zojax="http://namespaces.zope.org/zojax"
  ...      i18n_domain="zojax.formatter">
  ...    <include package="zojax.controlpanel" file="meta.zcml" />
  ...  <zojax:configlet
  ...     name="formatter"
  ...     schema="zojax.formatter.interfaces.IFormatterConfiglet"
  ...     title="Portal formatters"
  ...     description="Configure portal formatters."/>
  ... </configure>""")

We'll try emulate <product-config zojax.formatter>

  >>> from zope.app.appsetup import product
  >>> product._configs['zojax.formatter'] = {
  ...   'timezone': u'UTC', 'timezoneFormat': '2', 'principalTimezone': 'true'}

Let's check this

   >>> product.getProductConfiguration('zojax.formatter')
   {'timezone': u'UTC', 'timezoneFormat': '2', 'principalTimezone': 'true'}


Usually initFormatter() function is colled during IDatabaseOpenedEvent event,
we simply call it directly:

   >>> from zojax.formatter.config import initFormatter
   >>> initFormatter(None)

Now we can get IFormatterConfiglet utility

   >>> from zope.component import getUtility
   >>> from zojax.formatter.interfaces import IFormatterConfiglet

   >>> configlet = getUtility(IFormatterConfiglet)

Setup request

   >>> from zope import interface
   >>> from zope.publisher.browser import TestRequest
   >>> from zope.annotation.interfaces import IAttributeAnnotatable

   >>> request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
   >>> interface.directlyProvides(request, IAttributeAnnotatable)

   >>> from pytz import UTC
   >>> from datetime import date, datetime, timedelta


DateTime formatter
------------------

   >>> from zojax.formatter.tests import ZPTPage
   >>> page = ZPTPage()
   >>> page.pt_edit(u'''
   ... <html>
   ...   <body>
   ...     <tal:block tal:content="structure formatter:dateTime,short:options/now" />
   ...     <tal:block tal:content="structure formatter:dateTime,medium:options/now" />
   ...     <tal:block tal:content="structure formatter:dateTime,long:options/now" />
   ...     <tal:block tal:content="structure formatter:dateTime,full:options/now" />
   ...     <tal:block tal:content="structure formatter:dateTime:options/now" />
   ...   </body>
   ... </html>''', 'text/html')

   >>> dt = datetime(2007, 1, 1, 0, 0, 0, tzinfo=UTC)
   >>> dt
   datetime.datetime(2007, 1, 1, 0, 0, tzinfo=<UTC>)

By default we use UTC timezone for output:

   >>> print page.render(request, now=dt)
   <html>
     <body>
        <span class="zojax-formatter-datetime" value="January 01, 2007 00:00:00 +0000" format="short" offset="0">01/01/07 12:00 AM</span>
        <span class="zojax-formatter-datetime" value="January 01, 2007 00:00:00 +0000" format="medium" offset="0">Jan 01, 2007 12:00:00 AM</span>
        <span class="zojax-formatter-datetime" value="January 01, 2007 00:00:00 +0000" format="long" offset="0">January 01, 2007 12:00:00 AM +0000</span>
        <span class="zojax-formatter-datetime" value="January 01, 2007 00:00:00 +0000" format="full" offset="0">Monday, January 01, 2007 12:00:00 AM UTC</span>
        <span class="zojax-formatter-datetime" value="January 01, 2007 00:00:00 +0000" format="medium" offset="0">Jan 01, 2007 12:00:00 AM</span>
     </body>
   </html>


If datetime object doesn't contain timezone information, UTC is used

   >>> print page.render(request, now=datetime(2007, 1, 1, 0, 0))
   <html>
     <body>
        <span class="zojax-formatter-datetime" value="January 01, 2007 00:00:00 +0000" format="short" offset="0">01/01/07 12:00 AM</span>
        <span class="zojax-formatter-datetime" value="January 01, 2007 00:00:00 +0000" format="medium" offset="0">Jan 01, 2007 12:00:00 AM</span>
        <span class="zojax-formatter-datetime" value="January 01, 2007 00:00:00 +0000" format="long" offset="0">January 01, 2007 12:00:00 AM +0000</span>
        <span class="zojax-formatter-datetime" value="January 01, 2007 00:00:00 +0000" format="full" offset="0">Monday, January 01, 2007 12:00:00 AM UTC</span>
        <span class="zojax-formatter-datetime" value="January 01, 2007 00:00:00 +0000" format="medium" offset="0">Jan 01, 2007 12:00:00 AM</span>
     </body>
   </html>


Now let's chane timezone to US/Pacific, we change only time zone
not datetime value

   >>> configlet.timezone = 'US/Pacific'

   >>> print page.render(request, now=dt)
   <html>
     <body>
        <span class="zojax-formatter-datetime" value="December 31, 2006 16:00:00 -0800" format="short" offset="-480">12/31/06 04:00 PM</span>
        <span class="zojax-formatter-datetime" value="December 31, 2006 16:00:00 -0800" format="medium" offset="-480">Dec 31, 2006 04:00:00 PM</span>
        <span class="zojax-formatter-datetime" value="December 31, 2006 16:00:00 -0800" format="long" offset="-480">December 31, 2006 04:00:00 PM -0800</span>
        <span class="zojax-formatter-datetime" value="December 31, 2006 16:00:00 -0800" format="full" offset="-480">Sunday, December 31, 2006 04:00:00 PM PST</span>
        <span class="zojax-formatter-datetime" value="December 31, 2006 16:00:00 -0800" format="medium" offset="-480">Dec 31, 2006 04:00:00 PM</span>
     </body>
   </html>


fancyDatetime formatter
-----------------------

   >>> now = datetime.now(UTC)

   >>> fpage = ZPTPage()
   >>> fpage.pt_edit(u'''
   ... <html>
   ...   <body>
   ...     <tal:block tal:content="structure formatter:fancyDatetime:options/now" />
   ...     <tal:block tal:content="structure formatter:fancyDatetime,short:options/now" />
   ...     <tal:block tal:content="structure formatter:fancyDatetime,medium:options/now" />
   ...     <tal:block tal:content="structure formatter:fancyDatetime,full:options/now" />
   ...   </body>
   ... </html>''', 'text/html')

Today's datetime

   >>> today = now - timedelta(hours=1)

   >>> print fpage.render(request, now=today)
   <html>
     <body>
       ...<span ...
       ...<span ...
       ...<span ...
       ...<span ...
     </body>
   </html>


Yesterday's datetime

   >>> yesterday = now - timedelta(hours=25)

   >>> print fpage.render(request, now=yesterday)
   <html>
     <body>
       ...<span ...
       ...<span ...
       ...<span ...
       ...<span ...
     </body>
   </html>


Default timezone is UTC

   >>> now = datetime.now(UTC)
   >>> print fpage.render(request, now=now)
   <html>
     <body>
       ...<span ...
       ...<span ...
       ...<span ...
       ...<span ...
     </body>
   </html>


Date formatter
--------------

   >>> datepage = ZPTPage()
   >>> datepage.pt_edit(u'''
   ... <html>
   ...   <body>
   ...     <tal:block tal:content="structure formatter:date:options/today" />
   ...     <tal:block tal:content="structure formatter:date,short:options/today" />
   ...   </body>
   ... </html>''', 'text/html')

   >>> d = date(2007, 1, 1)
   >>> d
   datetime.date(2007, 1, 1)

   >>> print datepage.render(request, today=d)
   <html>
     <body>
       <span class="zojax-formatter-date" value="January 01, 2007 00:00:00 " format="medium">Jan 01, 2007</span>
       <span class="zojax-formatter-date" value="January 01, 2007 00:00:00 " format="short">01/01/07</span>
     </body>
   </html>


Also you can get formatter from python code

   >>> from zojax.formatter.utils import getFormatter
   >>> formatter = getFormatter(request, 'dateTime', 'full')
   >>> formatter.format(dt)
   u'<span class="zojax-formatter-datetime" value="December 31, 2006 16:00:00 -0800" format="full" offset="-480">Sunday, December 31, 2006 04:00:00 PM PST</span>'

We will get FormatterNotDefined if formatter is unknown

   >>> getFormatter(request, 'unknown')
   Traceback (most recent call last):
   ...
   FormatterNotDefined: ...

Wrong format, we should add path expression

   >>> errpage = ZPTPage()
   >>> errpage.pt_edit(u'''
   ...     <tal:block tal:content="formatter:unknown" />''', 'text/html')
   >>> print errpage.render(request)
   Traceback (most recent call last):
   ...
   PTRuntimeError: ...

Unknown formatter

   >>> errpage = ZPTPage()
   >>> errpage.pt_edit(u'''
   ...     <tal:block tal:content="formatter:unknown:opitons/now" />''', 'text/html')
   >>> print errpage.render(request)
   Traceback (most recent call last):
   ...
   FormatterNotDefined: unknown


Time formatter
--------------

   >>> datepage = ZPTPage()
   >>> datepage.pt_edit(u'''
   ... <html>
   ...   <body>
   ...     <tal:block tal:content="formatter:time:options/time" />
   ...     <tal:block tal:content="formatter:time,short:options/time" />
   ...   </body>
   ... </html>''', 'text/html')

   >>> t = datetime(2007, 1, 1, 10, 34, 03)
   >>> t
   datetime.datetime(2007, 1, 1, 10, 34, 3)

   >>> print datepage.render(request, time=t)
   <html>
     <body>
       10:34:03 AM
       10:34 AM
     </body>
   </html>


Custom formatter
================

We should define formatter factory and formatter itself
Let's implement formatter that accept string and currency name and
format as currency. Format of TALES expression whould be as
'formatter:<formatter name>,<formatter var1>,<formatter var2>,...:<path expression>'
<formatter name> is name of adapter that adapts IHTTPRequest to IFormatterFactory
also expression will pass <formatter var[1-...]> as args to factory.

   >>> from zojax.formatter.interfaces import IFormatter, IFormatterFactory

Here code of formatter:

   >>> class MyFormatter(object):
   ...    interface.implements(IFormatter)
   ...
   ...    currencies = {'usd': '$', 'euro': 'Eur'}
   ...
   ...    def __init__(self, request, *args):
   ...       self.request = request
   ...       self.currency = self.currencies[args[0]]
   ...
   ...    def format(self, value):
   ...       return '%s %s'%(value, self.currency)

Now we need formatter factory:

   >>> class MyFormatterFactory(object):
   ...    interface.implements(IFormatterFactory)
   ...
   ...    def __init__(self, request):
   ...        self.request = request
   ...
   ...    def __call__(self, *args, **kw):
   ...        return MyFormatter(self.request, *args)

Now we need register factory as named adapter for IHTTPRequest

   >>> from zope.component import provideAdapter
   >>> from zope.publisher.interfaces.http import IHTTPRequest

   >>> provideAdapter(MyFormatterFactory, \
   ...   (IHTTPRequest,), IFormatterFactory, name='currency')

Now we can use formatter

   >>> page = ZPTPage()
   >>> page.pt_edit(u'''<tal:block tal:define="value python:121.04">
   ... <tal:block tal:content="formatter:currency,usd:value" />
   ... <tal:block tal:content="formatter:currency,euro:value" />
   ... </tal:block>''', 'text/html')

   >>> print page.render(request)
   121.04 $
   121.04 Eur


humanDatetime formatter
-----------------------

   >>> now = datetime.now(UTC)

   >>> fpage = ZPTPage()
   >>> fpage.pt_edit(u'''
   ... <html>
   ...   <body>
   ...     <tal:block tal:content="structure formatter:humanDatetime:options/now" />
   ...     <tal:block tal:content="structure formatter:humanDatetime,short:options/now" />
   ...     <tal:block tal:content="structure formatter:humanDatetime,medium:options/now" />
   ...     <tal:block tal:content="structure formatter:humanDatetime,full:options/now" />
   ...   </body>
   ... </html>''', 'text/html')

Now datetime

   >>> print fpage.render(request, now=now)
   <html>
      <body>
        <span class="zojax-formatter-humandatetime" value="...">0 second(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">0 second(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">0 second(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">0 second(s) ago</span>
      </body>
    </html>

   >>> today = now - timedelta(seconds=1)

   >>> print fpage.render(request, now=today)
   <html>
      <body>
        <span class="zojax-formatter-humandatetime" value="...">1 second(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">1 second(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">1 second(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">1 second(s) ago</span>
      </body>
    </html>

   >>> today = now - timedelta(minutes=1)

   >>> print fpage.render(request, now=today)
   <html>
      <body>
        <span class="zojax-formatter-humandatetime" value="...">1 minute(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">1 minute(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">1 minute(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">1 minute(s) ago</span>
      </body>
    </html>

   >>> today = now - timedelta(hours=1)

   >>> print fpage.render(request, now=today)
   <html>
      <body>
        <span class="zojax-formatter-humandatetime" value="...">1 hour(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">1 hour(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">1 hour(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">1 hour(s) ago</span>
      </body>
    </html>

   >>> today = now - timedelta(days=1)

   >>> print fpage.render(request, now=today)
   <html>
      <body>
        <span class="zojax-formatter-humandatetime" value="...">1 day(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">1 day(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">1 day(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">1 day(s) ago</span>
      </body>
    </html>

   >>> today = now - timedelta(days=7)

   >>> print fpage.render(request, now=today)
   <html>
      <body>
        <span class="zojax-formatter-humandatetime" value="...">1 week(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">1 week(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">1 week(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">1 week(s) ago</span>
      </body>
    </html>

   >>> today = now - timedelta(days=30)

   >>> print fpage.render(request, now=today)
   <html>
      <body>
        <span class="zojax-formatter-humandatetime" value="...">1 month(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">1 month(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">1 month(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">1 month(s) ago</span>
      </body>
    </html>

   >>> today = now - timedelta(days=367)

   >>> print fpage.render(request, now=today)
   <html>
      <body>
        <span class="zojax-formatter-humandatetime" value="...">1 year(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">1 year(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">1 year(s) ago</span>
        <span class="zojax-formatter-humandatetime" value="...">1 year(s) ago</span>
      </body>
    </html>

Tomorrow's datetime

   >>> today = now + timedelta(seconds=1)

   >>> print fpage.render(request, now=today)
   <html>
      <body>
        <span class="zojax-formatter-humandatetime" value="...">in 1 second(s)</span>
        <span class="zojax-formatter-humandatetime" value="...">in 1 second(s)</span>
        <span class="zojax-formatter-humandatetime" value="...">in 1 second(s)</span>
        <span class="zojax-formatter-humandatetime" value="...">in 1 second(s)</span>
      </body>
    </html>

   >>> today = now + timedelta(minutes=1)

   >>> print fpage.render(request, now=today)
   <html>
      <body>
        <span class="zojax-formatter-humandatetime" value="...">in 1 minute(s)</span>
        <span class="zojax-formatter-humandatetime" value="...">in 1 minute(s)</span>
        <span class="zojax-formatter-humandatetime" value="...">in 1 minute(s)</span>
        <span class="zojax-formatter-humandatetime" value="...">in 1 minute(s)</span>
      </body>
    </html>

   >>> today = now + timedelta(hours=1)

   >>> print fpage.render(request, now=today)
   <html>
      <body>
        <span class="zojax-formatter-humandatetime" value="...">in 1 hour(s)</span>
        <span class="zojax-formatter-humandatetime" value="...">in 1 hour(s)</span>
        <span class="zojax-formatter-humandatetime" value="...">in 1 hour(s)</span>
        <span class="zojax-formatter-humandatetime" value="...">in 1 hour(s)</span>
      </body>
    </html>

   >>> today = now + timedelta(days=1)

   >>> print fpage.render(request, now=today)
   <html>
      <body>
        <span class="zojax-formatter-humandatetime" value="...">in 1 day(s)</span>
        <span class="zojax-formatter-humandatetime" value="...">in 1 day(s)</span>
        <span class="zojax-formatter-humandatetime" value="...">in 1 day(s)</span>
        <span class="zojax-formatter-humandatetime" value="...">in 1 day(s)</span>
      </body>
    </html>

  >>> today = now + timedelta(days=7)

  >>> print fpage.render(request, now=today)
   <html>
      <body>
        <span class="zojax-formatter-humandatetime" value="...">in 1 week(s)</span>
        <span class="zojax-formatter-humandatetime" value="...">in 1 week(s)</span>
        <span class="zojax-formatter-humandatetime" value="...">in 1 week(s)</span>
        <span class="zojax-formatter-humandatetime" value="...">in 1 week(s)</span>
      </body>
    </html>

  >>> today = now + timedelta(days=30)

  >>> print fpage.render(request, now=today)
   <html>
      <body>
        <span class="zojax-formatter-humandatetime" value="...">in 1 month(s)</span>
        <span class="zojax-formatter-humandatetime" value="...">in 1 month(s)</span>
        <span class="zojax-formatter-humandatetime" value="...">in 1 month(s)</span>
        <span class="zojax-formatter-humandatetime" value="...">in 1 month(s)</span>
      </body>
    </html>

  >>> today = now + timedelta(days=365)

  >>> print fpage.render(request, now=today)
   <html>
      <body>
        <span class="zojax-formatter-humandatetime" value="...">in 1 year(s)</span>
        <span class="zojax-formatter-humandatetime" value="...">in 1 year(s)</span>
        <span class="zojax-formatter-humandatetime" value="...">in 1 year(s)</span>
        <span class="zojax-formatter-humandatetime" value="...">in 1 year(s)</span>
      </body>
    </html>