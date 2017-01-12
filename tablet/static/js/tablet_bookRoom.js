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
    loadEvents();
});

function loadEvents(booking_id) {
    alert("HER");
    $('#calendar').fullCalendar("removeEvents");
    var start = $('#calendar').fullCalendar('getDate').startOf('month').format("DD-MM-YYYY");
    var end = $('#calendar').fullCalendar('getDate').endOf('month').format("DD-MM-YYYY");
    var data = {
        room_name: $('input[id=room_name]').val(),
        start: start,
        end: end,
    };
    getJSON(data,function(json){
        $.each(json, function(index, item) {
            var title = item.description
            var start = item.date + "T" + item.start_time;
            var end = item.date + "T" + item.end_time;
            var event = {
                id: item.booking_ref,
                title: item.description,
                start: new Date(start),
                end: new Date(end),
                isUserCreated: true,
                editable: false,
            };
            if (booking_id != "undefined" && event.id == booking_id){
                event.editable = true;
                event.color = "#66cc00";
            }
            $('#calendar').fullCalendar('renderEvent', event);
        });
    });
}

var getJSON = function(data,callback){
    $.ajax({
        type: 'POST',
        url: /getBookings/,
        dataType: 'json',
        data: data,
        success: function(data){
            callback(data);
        },
    });
    return false;
}