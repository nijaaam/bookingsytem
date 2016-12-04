function loadEvents() {
    var start = $('#calendar').fullCalendar('getDate').startOf('month').format("YYYY-MM-DD");
    var end = $('#calendar').fullCalendar('getDate').endOf('month').format("YYYY-MM-DD");
    var data = {
        room_name: $('#room_name').text(),
        start: start,
        end: end,
    };
    performAJAX('/getBookings/', 'json', data, callback);
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
        loadEvents();
    } else if (this.id == 'week') {
        view = 'agendaWeek';
    }
    $('#calendar').fullCalendar('changeView', view);
    updateTitle();
    return false;
});

var callback = function(data){
    var events = [];
    $.each(data, function(index,item){
        var title = item.description
        var start = item.date+"T"+item.start_time;
        var end = item.date+"T"+item.end_time;
        events.push({
            title: item.description,
            start: new Date(start),
            end: new Date(end),
        });
    });
    $('#calendar').fullCalendar("removeEvents");        
    $('#calendar').fullCalendar('addEventSource', events);      
    $('#calendar').fullCalendar('refetchEvents');
};
