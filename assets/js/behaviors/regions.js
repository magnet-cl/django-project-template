// Constants
const SELECT2_DEFAULT_OPTIONS = {
  width: '100%',
  theme: 'bootstrap-5'
};

// Initialize behavior
window.addEventListener('DOMContentLoaded', () => {
  const regionSearchSelector = '#id_region';
  const communeSearchSelector = '#id_commune';

  $(communeSearchSelector).select2({
    ...SELECT2_DEFAULT_OPTIONS,
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
    placeholder: 'Comuna'
  });

  $(regionSearchSelector).select2({
    ...SELECT2_DEFAULT_OPTIONS,
    placeholder: 'Región'
  });
});
