$(document).ready(function() {
    $.ajax({
        type: "get",
        url: "/showWeek/",
        dataType: "html",
        success: function(data) {
            $('#upcomingEvents').html(data);
        },
    });
    $.validator.addMethod("checkIfEmpty",function(value,element){
        if ($('input[name=duration_radio]:checked').val() == "userDuration"){
            var timeValue = $('input[name=durValue]').val();
            if (timeValue == ""){
                return false;
            }
        }
        return true;
    },"This field is required.");
    
    $.validator.addMethod("checkIfValidFormat",function(value,element){
        if ($('input[name=duration_radio]:checked').val() == "userDuration"){
            var timeValue = $('input[name=durValue]').val();
            var regex = new RegExp('(1?[0-9]|2[0-3]):[0-5][0-9]');
            if (regex.test(timeValue) == false){
                return false;
            }
        }
        return true;
    },"Invalid Format");
    $("#booking_details").validate({
        rules: {
            'contact': {
                required: true
            },
            'description': {
                required: true
            },
            'duration_radio': {
                required: true,
                checkIfEmpty: true,
                checkIfValidFormat: true,
            },
        },
        highlight: function(element,errorClass,validClass) {
            alert("HIGH" + element.name);
            if (element.name == "duration_radio"){
                $(element).closest('.form-group').addClass('has-error');
            } else if (element.name == "durValue"){
                $(element).closest('.form-group').addClass('has-error');
            } else {
                var error = "#" + $(element).attr("id") + "_error";
                $(element).closest('.form-group').removeClass('has-success').addClass('has-error has-feedback');
                $(error).addClass('glyphicon-remove');
            }
        },
        unhighlight: function(element,errorClass,validClass) {
            alert("UNHIGH" + element.name);
            if (element.name == "duration_radio"){
                //$(element).closest('.form-group').removeClass('has-error');
                $(element).closest('.form-group').remove('span');
            } else if (element.name == "durValue"){
                if (validateTime(element.value)){
                    $('input[name=durValue]:last').next().remove('span');
                }
            } else {
               var error = "#" + $(element).attr("id") + "_error";
               $(element).closest('.form-group').removeClass('has-error has-feedback');
               $(error).removeClass('glyphicon-remove'); 
            } 
        },
        errorElement: 'span',
        errorClass: 'help-block',
        errorPlacement: function(error, element) {
            if (element.attr("type") == "radio") {
                error.insertAfter($('input[name=durValue]:last'));
            } else {
                if (element.parent('.input-group').length) {
                    error.insertAfter(element.parent());
                } else {
                    error.insertAfter(element);
                }
            }
        },
    });
});

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