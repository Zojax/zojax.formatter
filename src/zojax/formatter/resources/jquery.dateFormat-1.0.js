(function ($) {
    $.format = (function () {

        var parseMonth = function (value) {
                       
            switch (value) {
            case "Jan":
                return "01";
            case "Feb":
                return "02";
            case "Mar":
                return "03";
            case "Apr":
                return "04";
            case "May":
                return "05";
            case "Jun":
                return "06";
            case "Jul":
                return "07";
            case "Aug":
                return "08";
            case "Sep":
                return "09";
            case "Oct":
                return "10";
            case "Nov":
                return "11";
            case "Dec":
                return "12";
            default:
                return value;
            }
        };
        
        var parseDay = function (value) {
            
            switch (value) {
            case "Mon":
                return 0;
            case "Tue":
                return 1;
            case "Wed":
                return 2;
            case "Thu":
                return 3;
            case "Fri":
                return 4;
            case "Sat":
                return 5;
            case "Sun":
                return 6;
            default:
                return value;
            }
        };
        
        var parseTime = function (value) {
            return {
                    hour: value.getHours(),
                    minute: value.getMinutes(),
                    second: value.getSeconds()
                };
            return {
                hour: "",
                minute: "",
                second: ""
            };
        };
        
        return {
            date: function (value, format) {
                //value = new java.util.Date()
                //2009-12-18 10:54:50.546
                try {
                    var year = null;
                    var short_year = null;
                    var month = null;
                    var dayOfMonth = null;
                    var dayOfWeek = null
                    var time = null; //json, time, hour, minute, second
                    if (typeof value.getFullYear != "function") {
                        var date = new Date();
                        date.setTime(Date.parse(value));
                        value = date
                    }
                    year = value.getFullYear().toString();
                    month = value.getMonth() + 1;
                    dayOfMonth = value.getDate();
                    dayOfWeek = value.getDay();
                    time = parseTime(value);
                    short_year = year.slice(2);
                    var pattern = "";
                    var retValue = "";
                    //Issue 1 - variable scope issue in format.date 
					//Thanks jakemonO
                    for (var i = 0; i < format.length; i++) {
                        var currentPattern = format.charAt(i);
                        pattern += currentPattern;
                        switch (pattern) {
                        case "E":
                            if (format.charAt(i+1) != 'E') {
                                retValue += day_names[dayOfWeek].slice(0, 3);
                                pattern = "";
                            }
                            break;
                        case "EEEE":
                            retValue += day_names[dayOfWeek];
                            pattern = "";
                            break;
                        case "d":
                            if (format.charAt(i+1) != 'd') {
                                retValue += dayOfMonth;
                                pattern = "";
                            }
                            break;
                        case "dd":
                            if (dayOfMonth < 10)
                                dayOfMonth = '0'+dayOfMonth;
                            retValue += dayOfMonth;
                            pattern = "";
                            break;
                        case "M":
                            if (format.charAt(i+1) != 'M'){
                                retValue += month;
                                pattern = "";
                            }
                            break;
                        case "MM":
                            if (format.charAt(i+1) != 'M'){
                                if (month < 10)
                                    month = '0'+month;
                                retValue += month;
                                pattern = "";
                            }
                            break;
                        case "MMM":
                            if (format.charAt(i+1) != 'M'){
                                retValue += month_names[month-1].slice(0, 3);
                                pattern = "";
                                break;
                            }
                            break;
                        case "MMMM":
                            retValue += month_names[month-1];
                            pattern = "";
                            break;
                        case "yy":
                            if (format.charAt(i+1) != 'y'){
                                retValue += short_year;
                                pattern = "";
                            }
                            break;
                        case "yyyy":
                            retValue += year;
                            pattern = "";
                            break;
                        case "H":
                            if (format.charAt(i+1) != 'H') {
                                retValue += time.hour;
                                pattern = "";
                            }
                            break;
                        case "HH":
                            retValue += time.hour;
                            pattern = "";
                            break;
                        case "hh":
                            retValue += (time.hour === 0 ? 12 : time.hour < 13 ? time.hour : time.hour - 12);
                            pattern = "";
                            break;
                        case "h":
                            if (format.charAt(i+1) != 'h') {
                                retValue += (time.hour === 0 ? 12 : time.hour < 13 ? time.hour : time.hour - 12);
                                pattern = "";
                            }
                            break;
                        case "mm":
                            retValue += time.minute;
                            pattern = "";
                            break;
                        case "ss":
                            retValue += time.second;
                            pattern = "";
                            break;
                        case "a":
                            retValue += time.hour > 12 ? "PM" : "AM";
                            pattern = "";
                            break;
                        case " ":
                            retValue += currentPattern;
                            pattern = "";
                            break;
                        case "-":
                            retValue += currentPattern;
                            pattern = "";
                            break;
                        case "/":
                            retValue += currentPattern;
                            pattern = "";
                            break;
                        case ":":
                            retValue += currentPattern;
                            pattern = "";
                            break;
                        case ",":
                            retValue += currentPattern;
                            pattern = "";
                            break;
                        case ".":
                            retValue += currentPattern;
                            pattern = "";
                            break;
                        }
                    }
                    return retValue;
                } catch (e) {
                    console.log(e);
                    return value;
                }
            }
        };
    }());
}(jQuery));


$(document).ready(function () {
    $(".shortDateFormat").each(function (idx, elem) {
        if ($(elem).is(":input")) {
            $(elem).val($.format.date($(elem).val(), 'dd/MM/yyyy'));
        } else {
            $(elem).text($.format.date($(elem).text(), 'dd/MM/yyyy'));
        }
    });
    $(".longDateFormat").each(function (idx, elem) {
        if ($(elem).is(":input")) {
            $(elem).val($.format.date($(elem).val(), 'dd/MM/yyyy hh:mm:ss'));
        } else {
            $(elem).text($.format.date($(elem).text(), 'dd/MM/yyyy hh:mm:ss'));
        }
    });
});

