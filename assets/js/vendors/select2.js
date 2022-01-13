export const SELECT2_DEFAULT_OPTIONS = {
  width: '100%',
  theme: 'bootstrap-5'
};

window.addEventListener('DOMContentLoaded', () => {
  const select2s = document.querySelectorAll('select:not(.js-not-select2)');

  select2s.forEach((select) => {
    $(select).select2(SELECT2_DEFAULT_OPTIONS);
  });
});
