$(document).ready(function() {
  const favicon = document.querySelector('[rel=icon]');

  if (favicon && favicon.href) {
    $('.favicon-ok').removeClass('d-none');
    $('favicon-href').html(favicon.href);
  } else {
    $('.favicon-not-ok').removeClass('d-none');
  }
});
