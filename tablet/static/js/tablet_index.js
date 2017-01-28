var footer_date = "";

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});


$(document).ready(function() {
    $('#cTime').html(new moment().format("HH:mm"));
    footer_date = new moment();
    $('#date_text').text(displayTime(footer_date));
    setInterval(function() {
        $('#cTime').html(new moment().format("HH:mm"));
    }, 1000);
    $('#next').click(function() {
        footer_date = footer_date.add(1, "days");
        $('#date_text').text(displayTime(footer_date));
        $('#scheduler').fullCalendar('gotoDate', footer_date);
        $('#scheduler').find('tbody .fc-scroller').css('height', 30);
        $('#scheduler').find('.fc-timeline-event').css('height', '24');
        $('#scheduler').find('.fc-timeline-event').css('overflow', 'hidden');
    });
    $('#prev').click(function() {
        footer_date = footer_date.subtract(1, "days");
        $('#date_text').text(displayTime(footer_date));
        $('#scheduler').fullCalendar('gotoDate', footer_date);
        $('#scheduler').find('tbody .fc-scroller').css('height', 30);
        $('#scheduler').find('.fc-timeline-event').css('height', '24');
        $('#scheduler').find('.fc-timeline-event').css('overflow', 'hidden');
    });
    var events = []
    $.each(bookings, function(index, item) {
        events.push({
            id: item.booking_ref,
            start: item.date + "T" + item.start_time,
            end: item.date + "T" + item.end_time,
            color: "#66cc00",
        });
    });
    $('#scheduler').fullCalendar({
        schedulerLicenseKey: 'CC-Attribution-NonCommercial-NoDerivatives',
        now: footer_date,
        contentHeight: 'auto',
        editable: false,
        aspectRatio: 1.8,
        filterResourcesWithEvents: false,
        allDaySlot: false,
        minTime: "07:00:00",
        maxTime: "20:00:00",
        header: {
            left: '',
            center: '',
            right: ''
        },
        defaultView: 'timelineDay',
        events: events,
    });
    $('#scheduler').find('tbody .fc-scroller').css('height', 30);
    $('#scheduler').find('.fc-timeline-event').css('height', '24');
    $('#scheduler').find('.fc-timeline-event').css('overflow', 'hidden');
});

$('#end').click(function() {
    $('#authModel').modal('show');
});
$("#search").on("input", function() {
    var str = $(this).closest('.form-group').attr('class');
    if (str.indexOf("has-error") >= 0) {
        var element = $('#search');
        $(element).closest('.form-group').removeClass('has-error has-feedback');
        $('#search_error').removeClass('glyphicon-remove');
        $('#ident_error').remove();
    }
});
function performAJAX(url, dataType, data, callback) {
    $.ajax({
        type: 'POST',
        url: url,
        dataType: dataType,
        data: data,
        success: callback,
    });
    return false;
}
$('#confirm').click(function() {
    performAJAX("/validateID/", "html", {
        'id': $('#search').val(),
    }, function(res) {
        if (res == "0") {
            var element = $('#search');
            $(element).closest('.form-group').removeClass('has-success').addClass('has-error has-feedback');
            $('#search_error').addClass('glyphicon-remove');
            $('<span id="ident_error" class="help-block">Identification Failed.</span>').insertAfter(element);
        } else {
            $('#authModel').modal('hide');
            end_event($('#booking_id').val());
        }
    });
    return false;
})

function end_event(id) {
    $.ajax({
        type: 'POST',
        dataType: 'html',
        url: 'end_event/',
        data: {
            'bk_id': id,
        },
        success: function() {
            var string = window.location.pathname;
            window.location = string;
        }
    });
}

function displayTime(t) {
    var time = t.format("HH:MM");
    var day_name = t.format('dddd');
    var day = t.format('DD');
    var month = t.format('MMM');
    return day_name + " " + day + " " + month;
}