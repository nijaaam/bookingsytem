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
        if ($('input[name=duration_radio]:checked').val() == "otherDuration"){
            var timeValue = $('input[name=durValue]').val();
            var regex = new RegExp('^(1?[0-9]|2[0-3]):[0-5][0-9]$');
            if (timeValue == ""){
                return true;
            }
        }
        return false;
    },"This field is required.");

    $.validator.addMethod("validateOtherDuration",function(value,element){
        if ($('input[name=duration_radio]:checked').val() == "otherDuration"){
            var timeValue = $('input[name=durValue]').val();
            var regex = new RegExp('(1?[0-9]|2[0-3]):[0-5][0-9]');
            if (regex.test(timeValue) == false){
                return false;
            }
        }
        return true;
    },"Enter a Valid Duration, XX:XX");
    
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
            },
        },
        highlight: function(element) {
            var error = "#" + $(element).attr("id") + "_error";
            $(element).closest('.form-group').removeClass('has-success').addClass('has-error');
            $(error).addClass('glyphicon-remove'); 
        },
        unhighlight: function(element,errorClass,validClass) {
            var error = "#" + $(element).attr("id") + "_error";
            $(element).closest('.form-group').removeClass('has-error has-feedback');
            $(error).removeClass('glyphicon-remove');
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
        }
    });
});

$("input[name=duration_radio]").click(function(){
    if (this.value == "otherDuration"){
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