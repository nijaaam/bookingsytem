function isMobile(){
    return (/Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent));
}

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
            if (item.id == booking_id){
                item.editable = true;
                item.color = "#A4E786";
            }
            $('#calendar').fullCalendar('renderEvent', item);
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
    if (!moment().isBefore(date,'day')){
        $('#prev').attr('disabled', true);
    } else {
        $('#prev').attr('disabled', false);
    }
    if (date.format("DD/MM/YYYY") == moment().format("DD/MM/YYYY")) {
        $('#today').attr('disabled', true);
    } else {
        $('#today').attr('disabled', false);
    }
    if ($('#calendar').fullCalendar('getView').name == 'month'){
        $('#month').click();
    }
    return false;
});

$('#day,#month,#week').click(function() {
    var view = 'month';
    if (this.id == 'day') {
        view = 'agendaDay';
    } else if (this.id == 'month'){
        loadEvents($('#booking_id').val());
    } else if (this.id == 'week') {
        view = 'agendaWeek';
    }
    $('#calendar').fullCalendar('changeView', view);
    updateTitle();
    return false;
});