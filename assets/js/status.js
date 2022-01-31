window.addEventListener('DOMContentLoaded', () => {
  const favicon = document.querySelector('[rel=icon]');
  const img = new Image();

  if (favicon && favicon.href) {
    document.querySelector('.favicon-ok').classList.remove('d-none');
    document.querySelector('.favicon-href').innerHTML = favicon.href;
  } else {
    document.querySelector('.favicon-not-ok').classList.remove('d-none');
  }

  const ogImage = document.querySelector('meta[name="og:image"]');

  if (ogImage && ogImage.content) {
    img.onload = function onload() {
      document.querySelector('.ogImage-not-ok').classList.add('d-none');

      if (this.width < 1080 || this.width !== this.height) {
        document.querySelector('.ogImage-warning').classList.remove('d-none');
      } else {
        document.querySelector('.ogImage-ok').classList.remove('d-none');
        document.querySelector('.ogImage-content').innerHTML = ogImage.content;
      }
    };

    img.src = ogImage.content;

    // in case everything fails
    document.querySelector('.ogImage-not-ok').classList.remove('d-none');
  } else {
    document.querySelector('.ogImage-not-ok').classList.remove('d-none');
  }
});
