window.addEventListener('DOMContentLoaded', () => {
  const regionSearchSelector = '#id_region';
  const communeSearchSelector = '#id_commune';

  $(communeSearchSelector).select2({
    ajax: {
      url: '/regions/communes/search/',
      dataType: 'json',
      delay: 250,
      data: (params) => ({
        commune: params.term,
        regionId: $(regionSearchSelector).val()
      }),
      processResults: (data) => ({ results: data }),
      cache: true
    },
    placeholder: 'Comuna',
    width: '100%'
  });

  $(regionSearchSelector).select2({
    placeholder: 'Región',
    width: '100%'
  });
});
