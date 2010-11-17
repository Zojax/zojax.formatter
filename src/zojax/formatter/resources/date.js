function setDateFormatter(el)
{
    el.text($.format.date(el.attr('value'), date_formats[el.attr('format')]));
    el.attr('processed', 'true')
}


$(document).ready(function() {
    var elems = $("span.zojax-formatter-date");
    for (var i = 0; i < elems.length; i++)
    {
        var el = $(elems[i]);
        if (!el.attr('processed')) {
            setDateFormatter(el);
        }
    }
});
