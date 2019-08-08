$(() => {
  const favicon = $('[rel=icon]')[0];
  const img = new Image();

  if (favicon && favicon.href) {
    $('.favicon-ok').removeClass('d-none');
    $('.favicon-href').html(favicon.href);
  } else {
    $('.favicon-not-ok').removeClass('d-none');
  }

  const ogImage = $('meta[name="og:image"]')[0];

  if (ogImage && ogImage.content) {
    img.onload = function onload() {
      $('.ogImage-not-ok').addClass('d-none');

      if (this.width < 1080 || this.width !== this.height) {
        $('.ogImage-warning').removeClass('d-none');
      } else {
        $('.ogImage-ok').removeClass('d-none');
        $('.ogImage-content').html(ogImage.content);
      }
    };

    img.src = ogImage.content;

    // in case everything fails
    $('.ogImage-not-ok').removeClass('d-none');
  } else {
    $('.ogImage-not-ok').removeClass('d-none');
  }
});
