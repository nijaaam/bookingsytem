function getUserBookings(id){
    performAJAX('/getUserBookings/','html',{
        'id': id,
    }, function (response){
        $('#userBookings').html(response);
    });
}
$('#search').on('typeahead:selected', function(e, datum) {
    getUserBookings(datum);
});

function testMoveEvent(id){
    var event = $('#calendar').fullCalendar('clientEvents',id);
    //alert(event[0].start);
    var start = event[0].start;
    var end = event[0].end;
    var new_start = start.add(15,'minutes');
    var new_end = end.add(30,'minutes');
    event[0].start = new_start;
    event[0].end  = new_end;
    var new_event = event[0];
    //alert(start.format("DD-MM-YYYYTHH:mm") + " " + end.format("DD-MM-YYYYTHH:mm") );
    $('#calendar').fullCalendar('updateEvent',event[0]);
}

function performAJAX(url, dataType, data, callback) {
    $.ajax({
        type: 'POST',
        url: url,
        dataType: dataType,
        data: data,
        success: callback,
    });
    return false;
}

$("#search").on("input", function() {
    var str = $(this).closest('.form-group').attr('class');
    if (str.indexOf("has-error") >= 0) {
        var element = $('#search');
        $(element).closest('.form-group').removeClass('has-error has-feedback');
        $('#search_error').removeClass('glyphicon-remove');
        $('#ident_error').remove();
    }
});

$('#booking_details').submit(function() {
    var event = $("#calendar").fullCalendar('clientEvents', "new_event")[0];
    if ($('#booking_details').valid() == true) {
        performAJAX("/validateID/", "html", {
            'id': $('#search').val(),
        }, function(res) {
            if (res == "0") {
                var element = $('#search');
                $(element).closest('.form-group').removeClass('has-success').addClass('has-error has-feedback');
                $('#search_error').addClass('glyphicon-remove');
                $('<span id="ident_error" class="help-block">Identification Failed.</span>').insertAfter(element);
            } else {
                var data = {
                    'start': event.start.format("HH:mm:ss"),
                    'end': event.end.format("HH:mm:ss"),
                    'date': $("#calendar").fullCalendar('getDate').format("YYYY-MM-DD"),
                    'id': $('#search').val(),
                };
                data = $('#booking_details').serialize() + '&' + $.param(data);
                performAJAX("/book_room/", "html", data, function(data) {
                    $('#showModal').html(data);
                    $('#modal').modal('show');
                });
            }
        });
    }
    return false;
});

$('#authUser').submit(function() {
    var user = $('#search').val();
    performAJAX("/validateID/", "html", {
        'id': user,
    }, function(res) {
        if (res == "0"){
            var element = $('#search');
            $(element).closest('.form-group').removeClass('has-success').addClass('has-error has-feedback');
            $('<span id="ident_error" class="help-block">Identification Failed.</span>').insertAfter(element.parent().parent());
        } else {
            getUserBookings(user);
        }
    });
    return false;
});

$('#findBookingForm').submit(function() {
    var callback = function(data) {
        $('#result').html(data);
    };
    performAJAX('/findBooking/', 'html', $('#findBookingForm').serialize(), callback);
    return false;
});

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            alert(cookieValue);
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

$('#cancelBooking').click(function() {
    $.ajax({
        type: 'POST',
        url: "/checkIfRecurring/",
        dataType: 'html',
        data: {
            "id": booking_id,
        },
        success: function(data) {
            if (data == "1") {
                $('#cancelBookingModal1').modal('show');
            } else {
                $('#cancelBookingModal').modal('show');
            }
        },
    });
});

$('#remAll,#remCurrent').click(function() {
    var deleteAll = false;
    if (this.id == "remAll") {
        deleteAll = true;
    }
    $.ajax({
        type: "POST",
        url: "/cancelBooking/",
        dataType: "html",
        data: {
            'id': booking_id,
            'deleteAll': deleteAll,
        },
        success: function(data) {
            if ($('#cancelBookingModal1').is(':visible')) {
                $('#modalText1').text(data);
                $('#remAll,#remCurrent').hide();
                $('#cancelBookingModal1').find("button#exit").text('Close');
            } else {
                $('#modalText').text(data);
                $('#remCurrent').hide();
                $('#cancelBookingModal').find("button#exit").text('Close');
            }
        }
    });
})

function getVAR(x) {
    var initial = $('#' + x).prop("defaultValue");
    var changed_val = $('#' + x).val();
    if (initial == changed_val) {
        return " ";
    } else {
        return changed_val;
    }
}

$('#update').click(function() {
    var booking = $("#calendar").fullCalendar('clientEvents', booking_id);
    var start = " ";
    var end = " ";
    var date = " ";
    var start = booking[0].start;
    if (start != undefined) {
        start = booking[0].start.format("HH:mm:ss");
        date = booking[0].start.format("YYYY-MM-DD");
        end = booking[0].end.format("HH:mm:ss");
    } else {
        start = " ";
    }
    $.ajax({
        type: "POST",
        url: "/updateBooking/",
        dataType: "html",
        data: {
            "description": getVAR('description'),
            "contact": getVAR('contact'),
            "start": start,
            "end": end,
            "date": date,
            "booking_id": booking_id,
        },
        success: function(data) {
            if ($('#viewBookingForm').valid()){
                $('#showUpdateBKModal').html(data);
            $('#updatedBKModal').modal('show');
            }
            
        },
    });
    return false;
});