var $datetimePicker = $('.datetime-picker');

if ($datetimePicker.datetimepicker) {
  $datetimePicker.datetimepicker({
    date: $datetimePicker.val(),
    format: 'DD/MM/YYYY HH:mm',
    locale: 'es'
  });
}

var $datePicker = $('.date-picker');
if ($datePicker.datetimepicker) {
  $datePicker.datetimepicker({
    date: $datePicker.val(),
    format: 'DD/MM/YYYY',
    locale: 'es'
  });
}

var $timePicker = $('.time-picker');
if ($timePicker.datetimepicker) {
  $timePicker.datetimepicker({
    date: $timePicker.val(),
    format: 'HH:mm',
    locale: 'es'
  });
}

$('.model-form input:text').addClass('form-control');

$('select').not('.js-not-select2').select2({
  width: '100%'
});

$('form').submit(function() {
  var $form = $(this);

  // disable buttons after submit to prevent disabling submit inputs
  // with values
  setTimeout(function() {
    $form
      .find(':submit')
      .not('.js-do-not-disable-on-submit')
      .addClass('disabled')
      .prop('disabled', true);
  }, 10);

  return true;
});
