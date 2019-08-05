$(() => {
  $('.datetimepicker-input').each((i, item) => {
    const $this = $(item);
    $this.data('target', `#${$this.prop('id')}`);

    $this.datetimepicker({
      date: moment($this.val(), 'DD/MM/YYYY').format('YYYY-MM-DD'),
      format: $this.data('format'),
      locale: 'es'
    });
  });
});
