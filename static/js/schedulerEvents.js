var insertEvents = function(json) {
    $.each(json, function(index, item) {
        $('#scheduler').fullCalendar('renderEvent', {
            id: item.booking_ref,
            resourceId: item.room_id,
            start: item.start_time,
            start: item.date + "T" + item.start_time,
            end: item.date + "T" + item.end_time,
            title: item.description,
            color: "#66cc00",
        });
    });
};  

$('#prev,#next,#today').unbind('click').click(function() {
    $('#scheduler').fullCalendar(this.id);
    var currentView = $('#scheduler').fullCalendar('getView');
    if (currentView.name == "month") {
        var start = $('#scheduler').fullCalendar('getDate').format("YYYY-MM-DD");
        var end = $('#scheduler').fullCalendar('getDate').endOf('month').format("YYYY-MM-DD");
        var data = {
            start: start,
            end: end,
        };
        performAJAX(/getRoomsBookings/, 'json', data, insertEvents);
    }
    $('#calendarDate').text(currentView.title);
    var date = $('#scheduler').fullCalendar('getDate');
    if (date.format("DD/MM/YYYY") == moment().format("DD/MM/YYYY")) {
        $('#today').attr('disabled', true);
    } else {
        $('#today').attr('disabled', false);
    }
    return false;
});

$('#day,#month,#week').unbind('click').click(function() {
    var view = 'month';
    if (this.id == 'day') {
        view = 'timelineDay';
        $('#scheduler').fullCalendar('option', 'contentHeight', height);
    } else if (this.id == 'month') {
        view = "month";
        $('#scheduler').fullCalendar('option', 'contentHeight', 'auto');
        $('#scheduler').fullCalendar("removeEvents");
        var start = $('#scheduler').fullCalendar('getDate').startOf('month').format("YYYY-MM-DD");
        var end = $('#scheduler').fullCalendar('getDate').endOf('month').format("YYYY-MM-DD");
        var data = {
            start: start,
            end: end,
        };
        performAJAX(/getRoomsBookings/, 'json', data, insertEvents);
    } else if (this.id == 'week') {
        view = 'agendaWeek';
        $('#scheduler').fullCalendar('option', 'contentHeight', 'auto');
    }
    $('#scheduler').fullCalendar('changeView', view);
    var currentView = $('#scheduler').fullCalendar('getView');
    $('#calendarDate').text(currentView.title);
    return false;
});