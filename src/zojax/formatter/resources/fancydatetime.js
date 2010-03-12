function setFancydatetimeFormatter(el)
{
    var date = new Date();
    date.setTime(Date.parse(el.text()));

    var now = new Date();

    delta = now-date;
    if (delta < 0) {
        delta = Math.abs(delta);
    }
    years = Math.floor(delta/(365*24*60*60*1000.0));
    months = Math.floor(delta/(30*24*60*60*1000.0));
    weeks = Math.floor(delta/(7*24*60*60*1000.0));
    days = Math.floor(delta/(24*60*60*1000.0));

    var res;

    if (!years && !months && !weeks && (now.getDay() != date.getDay())) {
        res = 'Yesterday at ' + date.toTimeString();

    } else if (!years && !months && !weeks && (now.getDay() == date.getDay())) {
        res = 'Today at ' + date.toTimeString();
    } else {
        res = el.attr('date') + ' ' + el.attr('time');
    }

    el.text(res);
    el.attr('processed', 'true')
}


$(document).ready(function() {
    
    var elems = $("span.zojax-formatter-fancydatetime");
    for (var i = 0; i < elems.length; i++)
    {
        var el = $(elems[i]);
        if (!el.attr('processed')) {
            setFancydatetimeFormatter(el);
        }
    }
});
