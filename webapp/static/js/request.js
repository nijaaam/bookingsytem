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
