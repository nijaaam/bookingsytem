function validateTime(time) {
    var arr = time.split(":");
    if (arr.length != 2) {
        return false;
    } else {
        if (isNaN(arr[0]) || isNaN(arr[1])) {
            return false;
        }
        if (arr[0] > 24 || arr[1] > 60 || arr[0] < 0 || arr[1] < 0) {
            return false;
        }
        if (arr[1].toString().length != 2) {
            return false;
        }
        if (arr[0].toString().length == 0) {
            return false;
        }
    }
    return true;
}

$("input[name=duration_radio]").click(function() {
    if (this.value == "userDuration") {
        $("input[name=durValue]").prop('disabled', false);
    } else {
        $("input[name=durValue]").val("");
        $("input[name=durValue]").prop('disabled', true);
    }
});

$('#booking_details').submit(function() {
    $.ajax({
        type: "POST",
        url: "/book_room/",
        dataType: "html",
        data: $('#booking_details').serialize(),
        success: function(data) {
            if ($('#booking_details').valid() == true) {
                $('#showModal').html(data);
                $('#modal').modal('show');
            }
        },
    });
    return false;
});

$('#findBookingForm').submit(function() {
    $.ajax({
        type: "POST",
        url: "/findBooking/",
        dataType: "html",
        data: $('#findBookingForm').serialize(),
        success: function(data) {
            $('#result').html(data);
        }
    });
    return false;
});


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
/*
$('#day,#month,#week').click(function(){
    var view = 'month';
    if (this.id == 'day'){
        view = 'agendaDay';
    } else if (this.id == 'month'){
        view = this.id;
    } else if (this.id == 'week'){
        view = this.id == 'agendaWeek';
    }
    $('#calendar').fullCalendar('changeView', view);
    var date = $('#calendar').fullCalendar('getDate').format("YYYY-MM-DD");
    var room_name = $('#room_name').text();
});
*/

function performAJAX(url,dataType,data,callback){
    $.ajax({
        type: 'POST',
        url: url,
        dataType: dataType,
        data: data,
        success: callback,
    });
}
$('#day').click(function() {
    $('#calendar').fullCalendar('changeView', 'agendaDay');
    var date = $('#calendar').fullCalendar('getDate').format("YYYY-MM-DD");
    var room_name = $('#room_name').text();
    updateTitle();
    var data = {
        day: date,
        room_name, room_name,
    };
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
    performAJAX('/getBookingsDay/','json',data,callback);
});

$('#month').click(function() {
    $('#calendar').fullCalendar('changeView', 'month');
    updateTitle();
});
$('#week').click(function() {
    $('#calendar').fullCalendar('changeView', 'agendaWeek');
    updateTitle();
});

$('#cancelBooking').click(function() {
    $('#cancelBookingModal').modal('show');
});

$('#cancelBooking2').click(function() {
    var booking_id = $('input[name=booking_id]').val();
    var input = $input = $('<input type="text" name="booking_id" hidden/>').val(booking_id);
    $('#viewBooking').append(input);
    $.ajax({
        type: "POST",
        url: "/cancelBooking/",
        dataType: "html",
        data: $('#viewBooking').serialize(),
        success: function(data) {
            $('#modalText').text(data);
            $('#cancelBooking2').remove();
            $('#exit').text('Close').button("refresh");
            $("[id='exit']").click(function() {
                window.location = "/";
            });
            $("[id='exit1']").click(function() {
                window.location = "/";
            });
        }
    });
});
