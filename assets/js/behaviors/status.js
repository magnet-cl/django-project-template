$(() => {
  const favicon = $('[rel=icon]')[0];
  if (favicon && favicon.href) {
    $('.favicon-ok').removeClass('d-none');
    $('.favicon-href').html(favicon.href);
  } else {
    $('.favicon-not-ok').removeClass('d-none');
  }
});
