window.addEventListener('DOMContentLoaded', () => {
  const select2s = document.querySelectorAll('select:not(.js-not-select2)');

  select2s.forEach((select) => {
    $(select).select2({
      width: '100%'
    });
  });
});
