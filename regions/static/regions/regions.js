(function() {
  'use strict';

  var regionSearchSelector = '#id_region';
  var communeSearchSelector = '#id_commune';

  /**
  * Fill communes by region selected
  * @param {Object} e
  */
  $(communeSearchSelector).select2({
    ajax: {
      url: '/regions/communes/search/',
      dataType: 'json',
      delay: 250,
      data: function(params) {
        return {
          commune: params.term,
          regionId: $(regionSearchSelector).val()
        };
      },

      processResults: function(data, params) {
        return {
          results: data
        };
      },

      cache: true
    },
    placeholder: 'Comuna',
    width: '100%'
  });

  $(regionSearchSelector).select2({
    placeholder: 'Región',
    width: '100%'
  });

})();
