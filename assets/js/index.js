import '../scss/main.scss';
import App from './app';

import './behaviors/status';
import './behaviors/input-time-picker';
import './behaviors/input-rut';

$(() => {
  $('.alert').each((i, item) => {
    App.utils.highlight($(item));
  });

  const $alert = $('.main-alert .alert');
  setTimeout(() => $alert.fadeOut(), 10000);

  $('.model-form input:text').addClass('form-control');

  $('select').not('.js-not-select2').select2({
    width: '100%'
  });

  $('form').submit((e) => {
    const $this = $(e.currentTarget);
    const $buttons = $this.find(':submit').not('.js-do-not-disable-on-submit');

    // disable buttons after submit to prevent disabling submit inputs
    // with values
    setTimeout(() => {
      $buttons.addClass('disabled').prop('disabled', true);
      App.utils.showLoading($buttons);

      setTimeout(() => {
        $buttons.removeClass('disabled').prop('disabled', false);
        App.utils.hideLoading();
      }, 3000);
    }, 10);

    return true;
  });
});
