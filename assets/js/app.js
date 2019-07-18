const App = {};

App.utils = {
  hideLoading() {
    $('body').removeClass('wait');
  },

  thousandSeparator(x) {
    return Math.round(x).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  },

  showLoading($element) {
    $('body').addClass('wait');

    if ($element && $element.find('.page-loading-icon').length === 0) {
      $element.append(
        '<i class="fa fa-spinner fa-spin page-loading-icon"></i>'
      );
    }
  },

  highlight($element) {
    $element.addClass('highlight');

    setTimeout(() => {
      $element.toggleClass('dim highlight');
    }, 15);

    setTimeout(() => $element.removeClass('dim'), 1010);
  }
};


export default App;
