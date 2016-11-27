function validateTime(time){
    var arr = time.split(":");
    if (arr.length != 2){
        return false;
    } else {
        if (isNaN(arr[0]) || isNaN(arr[1])){
            return false;
        } if (arr[0] > 24 || arr[1] > 60 || arr[0] < 0 || arr[1] < 0){
            return false;
        } if (arr[1].toString().length != 2){
            return false;
        } if (arr[0].toString().length == 0){
            return false;
        }
    }
    return true;
}

$("input[name=duration_radio]").click(function(){
    if (this.value == "userDuration"){
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
            if ($('#booking_details').valid() == true){
                $('#showModal').html(data);
                $('#modal').modal('show');
            }
        },
    });
    return false;
});

$('#findBookingForm').submit(function(){
    $.ajax({
        type: "POST",
        url: "/findBooking/",
        dataType: "html",
        data: $('#findBookingForm').serialize(),
        success: function(data){
            $('#result').html(data);
        }
    });
    return false;
});