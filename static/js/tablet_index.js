var footer_date = "";
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


function end_event() {
    $.ajax({
        type: 'POST',
        dataType: 'html',
        url: 'end_event/',
        data: {
            'bk_id': id,
        },
    });
}

function displayTime(t) {
    var time = t.format("HH:MM");
    var day_name = t.format('dddd');
    var day = t.format('DD');
    var month = t.format('MMM');
    return day_name + " " + day + " " + month;
}