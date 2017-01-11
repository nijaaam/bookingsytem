$(document).ready(function() {
    $('#cTime').html(new moment().format("HH:mm"));
    setInterval(function() {
        $('#cTime').html(new moment().format("HH:mm"));
    }, 1000);
    settings.defaultDate = datetime;
    settings.eventConstraint = {
        start: moment().subtract(5, 'minutes'),
        end: moment().add(1, 'year'),
    };
    var updateTimes = function(event, delta, revertFunc) {
        var start = event.start.format("HH:mm");
        var end = event.end.format("HH:mm");
        $('#start').html(start);
        $('#end').html(end);
    };
    settings.eventDrop = updateTimes;
    settings.eventResize = updateTimes;
    $('#calendar').fullCalendar(settings);
    var newEvent = {
        id: "new_event",
        editable: true,
        color: "#66cc00",
    };
    newEvent.start = datetime.format("YYYY-MM-DDTHH:mm:ss");
    newEvent.end = datetime.add(15, 'minutes').format("YYYY-MM-DDTHH:mm:ss");
    $('#calendar').fullCalendar('renderEvent', newEvent);
    $('#month').unbind('click').click(function() {
        $('#calendar').fullCalendar('changeView', 'month');
        updateTitle();
        loadEvents();
        $('#calendar').fullCalendar('renderEvent', newEvent);
    });
});