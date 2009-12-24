var formatter_past_dictionary = {
    '%s year(s) ago'  : '%s year(s) ago',
    '%s month(s) ago'  : '%s month(s) ago',
    '%s week(s) ago': '%s week(s) ago',
    '%s day(s) ago' : '%s day(s) ago',
    '%s hour(s) ago' : '%s hour(s) ago',
    '%s minute(s) ago' : '%s minute(s) ago',
    '%s second(s) ago' : '%s second(s) ago'
};

var formatter_future_dictionary = {
    '%s year(s) ago'  : '%s year(s) ago',
    '%s month(s) ago'  : '%s month(s) ago',
    '%s week(s) ago': '%s week(s) ago',
    '%s day(s) ago' : '%s day(s) ago',
    '%s hour(s) ago' : '%s hour(s) ago',
    '%s minute(s) ago' : '%s minute(s) ago',
    '%s second(s) ago' : '%s second(s) ago'
};

function setHumandatetimeFormatter(el)
{
    var time = new Date();
    time.setTime(Date.parse(el.attr('value')));
    var new_time = new Date();
    delta = new_time-time;
    $.i18n.setDictionary(formatter_past_dictionary);
    if (delta < 0) {
        delta = Math.abs(delta);
        $.i18n.setDictionary(formatter_future_dictionary)
    }
    years = Math.floor(delta/(365*24*60*60*1000.0));
    months = Math.floor(delta/(30*24*60*60*1000.0));
    weeks = Math.floor(delta/(7*24*60*60*1000.0));
    days = Math.floor(delta/(24*60*60*1000.0));
    hours = Math.floor(delta/(60*60*1000.0));
    minutes = Math.floor(delta/(60*1000.0));
    seconds = Math.floor(delta/(1000.0));
    var res;
    if (years)
        res = $.i18n._('%s year(s) ago', [years])
    else if (months)
        res = $.i18n._('%s month(s) ago', [months])
    else if (weeks)
        res = $.i18n._('%s week(s) ago', [weeks])
    else if (days)
        res = $.i18n._('%s day(s) ago', [days])
    else if (hours)
        res = $.i18n._('%s hour(s) ago', [hours])
    else if (minutes)
        res = $.i18n._('%s minute(s) ago', [minutes])
    else
        res = $.i18n._('%s second(s) ago', [seconds])
    el.text(res);
    el.attr('processed', 'true')
}


$(document).ready(function() {
    var elems = $("span.zojax-formatter-humandatetime");
    for (var i = 0; i < elems.length; i++)
    {
        var el = $(elems[i]);
        if (!el.attr('processed')) {
            setHumandatetimeFormatter(el);
        }
    }
});