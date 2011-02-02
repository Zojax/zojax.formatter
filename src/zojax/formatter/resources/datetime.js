function setDatetimeFormatter(el)
{
    var date = new Date();
    date.setTime(Date.parse(el.text()));
    
    var now = new Date();
    var time = date.getTime()+now.getTimezoneOffset() - 60*1000*(parseInt(el.attr('offset')));
    date.setTime(time);
    var time_string = $.format.date(date, time_formats[el.attr('format')]);

    el.text($.format.date(el.attr('value'), datetime_formats[el.attr('format')]))
    el.attr('processed', 'true')
}


$(document).ready(function() {
    
    var elems = $("span.zojax-formatter-datetime");
    for (var i = 0; i < elems.length; i++)
    {
        var el = $(elems[i]);
        if (!el.attr('processed')) {
            setDatetimeFormatter(el);
        }
    }
});
