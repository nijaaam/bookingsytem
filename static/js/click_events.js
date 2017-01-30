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
            if ($('#viewBookingForm').valid()) {
                $('#showUpdateBKModal').html(data);
                $('#updatedBKModal').modal('show');
            }

        },
    });
    return false;
});

$('#openCal').click(function() {
    $('#toolbar').show();
    loadCalendar();
    $('html,body').animate({
        scrollTop: $("#calendar").offset().top
    });
});