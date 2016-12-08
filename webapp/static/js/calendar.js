function loadEvents(booking_id) {
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
            alert(item);
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

function updateTitle() {
    var currentView = $('#calendar').fullCalendar('getView');
    $('#calendarDate').text(currentView.title);
}

$('#prev,#next,#today').click(function() {
    $('#calendar').fullCalendar(this.id);
    updateTitle();
    var date = $('#calendar').fullCalendar('getDate');
    if (date.format("DD/MM/YYYY") == moment().format("DD/MM/YYYY")) {
        $('#today').attr('disabled', true);
    } else {
        $('#today').attr('disabled', false);
    }
    return false;
});

$('#day,#month,#week').click(function() {
    var view = 'month';
    if (this.id == 'day') {
        view = 'agendaDay';
    } else if (this.id == 'month') {
        view = this.id;
        loadEvents(booking_id.value);
    } else if (this.id == 'week') {
        view = 'agendaWeek';
    }
    $('#calendar').fullCalendar('changeView', view);
    updateTitle();
    return false;
});
