var $datetimePicker = $('.datetime-picker');
if ($datetimePicker.datetimepicker) {
    $datetimePicker.datetimepicker({
        date: $datetimepicker.val(),
        format: 'DD/MM/YYYY HH:mm',
        locale: 'es'
    });
}

var $datePicker = $('.date-picker');
if ($datePicker.datetimepicker) {
    $datePicker.datetimepicker({
        date: $datepicker.val(),
        format: 'DD/MM/YYYY',
        locale: 'es'
    });
}

var $timePicker = $('.time-picker');
if ($timePicker.datetimepicker) {
    $timePicker.datetimepicker({
        date: $timepicker.val(),
        format: 'HH:mm',
        locale: 'es'
    });
}

$('.model-form input:text').addClass('form-control');

$('select').not('.not-select2').select2({
    width: "100%"
});
