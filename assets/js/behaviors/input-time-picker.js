$(() => {
  $('.datetimepicker-input').each((i, item) => {
    const $this = $(item);
    $this.data('target', `#${$this.prop('id')}`);

    $this.datetimepicker({
      date: $this.val(),
      format: $this.data('format'),
      locale: 'es'
    });
  });
});
