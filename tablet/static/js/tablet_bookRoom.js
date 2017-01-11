$(document).ready(function() {
	$('#cTime').html(new moment().format("HH:mm"));
	setInterval(function() {
	    $('#cTime').html(new moment().format("HH:mm"));
	}, 1000);
	settings.defaultDate = datetime;
    settings.events = bookings;
    $('#calendar').fullCalendar(settings);
    $('#calendar').fullCalendar('renderEvent', {
        id : "new_event",
        editable: true,
        color: "#66cc00",
        start: datetime.format("YYYY-MM-DDTHH:mm:ss"),
        end : datetime.add(15, 'minutes').format("YYYY-MM-DDTHH:mm:ss"),
    });
});
