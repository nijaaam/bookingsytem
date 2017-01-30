$.validator.setDefaults({
    highlight: function(element, errorClass, validClass) {
        var error = "#" + $(element).attr("id") + "_error";
        $(element).closest('.form-group').removeClass('has-success').addClass('has-error has-feedback');
        $(error).addClass('glyphicon-remove');
    },
    unhighlight: function(element, errorClass, validClass) {
        var error = "#" + $(element).attr("id") + "_error";
        $(element).closest('.form-group').removeClass('has-error has-feedback');
        $(error).removeClass('glyphicon-remove');
    },
    errorElement: 'span',
    errorClass: 'help-block',
    errorPlacement: function(error, element) {
        if (element.parent('.input-group').length) {
            error.insertAfter(element.parent());
        } else {
            error.insertAfter(element);
        }
    },
});

$('#authUser').validate({
    rules: {
        'search': {
            required: true,
        }
    },
});

$("#singupForm").validate({
    rules: {
        'id_name': {
            required: true
        },
        'id_email': {
            required: true,
            email: true,
        },
    },
});

$.validator.addMethod("validate_date", function(value, element) {
    if ($('#recurring').val() != 0) {
        var input = $('#end').val();
        if (input == "") {
            return false;
        } else {
            return true;
        }
    } else {
        return true;
    }
}, "This field is required");

$("#booking_details").validate({
    rules: {
        'contact': {
            required: true
        },
        'description': {
            required: true
        },
        'recurr_end': {
            validate_date: true,
        },
        'search': {
            required: true,
        }
    },
});

$("#viewBookingForm").validate({
    rules: {
        'contact': {
            required: true
        },
        'description': {
            required: true
        },
    },
});