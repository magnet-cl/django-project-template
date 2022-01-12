/**
 * Initialize `input` as a Tempus Dominus datetime picker
 * @param {HTMLInputElement} input
 * @return {datetimepicker}
 */
function initDatetimePickerInput(input) {
  const { format } = input.dataset;
  const date = moment(input.value, format);

  input.dataset.target = `#${input.id}`; // eslint-disable-line no-param-reassign

  return $(input).datetimepicker({
    date,
    format,
    locale: document.documentElement.lang
  });
}

// Initialize behavior
window.addEventListener('DOMContentLoaded', () => {
  const datetimepickerInputs = document.querySelectorAll('.datetimepicker-input');

  datetimepickerInputs.forEach(initDatetimePickerInput);
});
