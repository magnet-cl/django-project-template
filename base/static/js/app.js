var App = {};

(function() {
  App.utils = {
    hideLoading: function() {
      $('body').removeClass('wait');
    },

    thousandSeparator: function(x) {
      x = Math.round(x);
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    },

    showLoading: function($element) {
      $('body').addClass('wait');

      if ($element && $element.find('.page-loading-icon').length === 0) {
        $element.append(
          '<i class="fa fa-spinner fa-spin page-loading-icon"></i>'
        );
      }
    },

    highlight: function($el) {
      $el.addClass('highlight');

      setTimeout(function() {
        $el.toggleClass('dim highlight');
      }, 15);

      setTimeout(function() {$el.removeClass('dim');}, 1010);
    }
  };

  $('.alert').each(function() {
    App.utils.highlight($(this));
  });
}());
