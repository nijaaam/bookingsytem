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
    $('#book').click(function(){
        var events = $('#calendar').fullCalendar( 'clientEvents',"new_event");
        var start = events[0].start;
        var end = events[0].end;
        var date = events[0].date;
        $.ajax({
            type: 'POST',
            dataType: 'html',
            data: {
                'start' : start.format('HH:mm'),
                'end':end.format('HH:mm'),
                'date':start.format('YYYY-MM-DD'),
            },
            url: '/tablet/quickBook/',
            success: function (data){
                $('#showModal').html(data);
                $('#modal').modal('show');
            },
        });
    });
    $('#cTime').html(new moment().format("HH:mm"));
    setInterval(function() {
        $('#cTime').html(new moment().format("HH:mm"));
    }, 1000);
    settings.defaultDate = datetime;
    alert(datetime);
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
    settings.dayClick = function(date, jsEvent, view) {
        if (date > moment()){
            var start = date.format("YYYY-MM-DDTHH:mm:ss");
            var end = date.add(15, 'minutes').format("YYYY-MM-DDTHH:mm:ss");
            start = new moment(start,"YYYY-MM-DDTHH:mm:ss");
            end = new moment(end,"YYYY-MM-DDTHH:mm:ss");
            var view = view.name;
            var event = $('#calendar').fullCalendar('clientEvents',"new_event");
            if (event != ""){
                $('#calendar').fullCalendar('removeEvents',"new_event");
            } 
            var newEvent = {
                id: "new_event",
                editable: true,
                color: "#66cc00",
            };
            newEvent.start = start;
            newEvent.end = end;
            updateTimes(newEvent,'','');
            $('#calendar').fullCalendar('renderEvent',newEvent);
        }
    }
    $('#calendar').fullCalendar(settings);
    updateTitle();
    loadEvents();
    var newEvent = {
        id: "new_event",
        editable: true,
        color: "#66cc00",
    };
    newEvent.start = datetime.format("YYYY-MM-DDTHH:mm:ss");
    newEvent.end = datetime.add(15, 'minutes').format("YYYY-MM-DDTHH:mm:ss");
    //$('#calendar').fullCalendar('renderEvent', newEvent);
    $('#month').unbind('click').click(function() {
        $('#calendar').fullCalendar('changeView', 'month');
        updateTitle();
        loadEvents();
        //$('#calendar').fullCalendar('renderEvent', newEvent);
    });
});

function loadEvents(booking_id) {
    $('#calendar').fullCalendar("removeEvents");
    var start = $('#calendar').fullCalendar('getDate').startOf('month').format("DD-MM-YYYY");
    var end = $('#calendar').fullCalendar('getDate').endOf('month').format("DD-MM-YYYY");
    var data = {
        room_name: $('#room_name').val(),
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