$(document).ready(function(){
	$.ajax({
        type: "get",
        url: "/showWeek/",
        dataType: "html",
        success: function(data){
            $('#upcomingEvents').html(data);
        },
    });
});

$('#booking_details').submit(function(){
	$.ajax({
		type: "POST",
		url: "/book_room/",
		dataType: "html",
		data: $('#booking_details').serialize(),
		success: function(data){
            $('#showModal').html(data);
            $('#modal').modal('show');
        },
	});
	return false;
});

