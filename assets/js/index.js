import '../scss/main.scss';
import App from './app';

// Vendors
import './vendors/select2';
import './vendors/tempus-dominus';

// Behaviors
import './behaviors/status';
import './behaviors/input-rut';

window.addEventListener('DOMContentLoaded', () => {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach((alert) => {
    App.utils.highlight(alert);
  });

  setTimeout(() => {
    const mainAlerts = document.querySelectorAll('.main-alert .alert');
    mainAlerts.forEach((alert) => {
      $(alert).alert('close');
    });
  }, 10000);

  document.querySelectorAll('form')
    .forEach((form) => {
      form.addEventListener('submit', () => {
        const submitButtons = [...form.elements].filter((element) => (
          element.matches('[type="submit"]:not(.js-do-not-disable-on-submit)')
        ));

        // Disable buttons after submit to prevent disabling submit inputs
        // with values
        submitButtons.forEach((submitButton) => {
          submitButton.disabled = true; // eslint-disable-line no-param-reassign
          App.utils.showLoading(submitButton);
        });

        return true;
      });
    });
});
