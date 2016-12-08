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