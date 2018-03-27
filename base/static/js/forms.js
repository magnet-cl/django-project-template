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
  var $buttons = $(this).find(':submit').not('.js-do-not-disable-on-submit');

  // disable buttons after submit to prevent disabling submit inputs
  // with values
  setTimeout(function() {
    $buttons.addClass('disabled').prop('disabled', true);
    window.App.utils.showLoading($buttons);

    setTimeout(function() {
      $buttons.removeClass('disabled').prop('disabled', false);
      window.App.utils.hideLoading();
    }, 3000);
  }, 10);

  return true;
});
