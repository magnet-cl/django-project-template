import '../scss/main.scss';

// Vendors
import './vendors/choices';
import './vendors/tempus-dominus';

// Behaviors
import './behaviors/input-rut';
import './behaviors/regions';

// Utils
import App from './utils/app';

window.addEventListener('DOMContentLoaded', () => {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach((alert) => {
    App.utils.highlight(alert);
  });

  setTimeout(() => {
    const mainAlerts = document.querySelectorAll('.main-alert .alert');
    mainAlerts.forEach((alert) => {
      bootstrap.Alert.getInstance(alert).close();
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
