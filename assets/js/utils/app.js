const App = {};

App.utils = {
  hideLoading() {
    document.body.classList.remove('wait');
  },

  thousandSeparator(x) {
    return Math.round(x).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  },

  showLoading(element) {
    document.body.classList.add('wait');

    if (!element.querySelector('.loading-icon')) {
      element.insertAdjacentHTML(
        'beforeend',
        '<span class="fas fa-spinner fa-spin loading-icon" aria-hidden="true"></span>'
      );
    }
  },

  highlight(element) {
    element.classList.add('highlight');

    setTimeout(() => {
      element.classList.add('dim');
      element.classList.remove('highlight');
    }, 15);

    setTimeout(() => element.classList.remove('dim'), 1010);
  }
};

export default App;
