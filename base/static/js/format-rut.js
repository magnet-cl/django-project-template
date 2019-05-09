class RutInput {
  constructor($rutInput) {
    this.$rutInput = $rutInput;
    this.$rutInputContainer = $rutInput.parent();
    this.$submitBtn = $rutInput.parents('form').find('[type="submit"]');

    this.errorMessage = '* RUT inválido.';
    this.$errorMessage = $(`<p class='form-error'>${this.errorMessage}</p>`);

    this.setListeners();
  }

  /**
   * Add event listeners
   */
  setListeners() {
    this.$rutInput.keyup(this.handleRut.bind(this));
    this.$rutInput.blur(this.handleRut.bind(this));
  }

  /**
   * Handle event listeners
   */
  handleRut() {
    this.formatRut();
    this.validateRut();
  }

  /**
   * Set input value with correct rut format
   */
  formatRut() {
    let rut = this.$rutInput.val().replace(/-/g, '');

    if (rut !== '' && rut.length > 1) {
      rut = rut.replace(/\./g, '');

      const digits = rut.slice(0, - 1).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
      const dv = rut.slice(- 1);

      this.$rutInput.val(`${digits}-${dv}`);
    }
  }

  /**
   * Check if input value is a valid rut
   * @return {boolean}
   */
  checkRut() {
    const rut = this.$rutInput.val()
      .replace(/-/g, '')
      .replace(/\./g, '');

    if (rut.length < 2) {
      return false;
    }

    const digits = rut.slice(0,-1);
    const dv = rut.slice(-1).toUpperCase();

    // calculate DV
    let sum = 0;
    let mult = 2;

    for (let i = digits.length -1; i >= 0; i -= 1) {
      sum = sum + parseInt(rut[i]) * mult;
      mult = ( mult + 1 ) % 8 || 2;
    }

    // check DV
    switch(sum % 11) {
      case 1 : return 'K' == dv;
      case 0 : return 0 == dv;
      default : return (11 - (sum % 11)) == dv;
    }
  }

  /**
   * Show error messagge
   */
  showRutError() {
    this.$rutInput.addClass('form-control-error');
    this.$submitBtn.prop('disabled', true);

    const $errorMessage = $(`<p class='form-error'>${this.errorMessage}</p>`);
    this.$rutInputContainer.append(this.$errorMessage);
  }

  /**
   * Hide error messagge
   */
  hideRutError() {
    this.$rutInput.removeClass('form-control-error');
    this.$rutInputContainer.find('.form-error').remove();
    this.$submitBtn.prop('disabled', false);
  }

  /**
   * Show error messagge if input value is not a correct rut
   */
  validateRut() {
    this.hideRutError();

    if (!this.checkRut()) {
      this.showRutError();
    }
  }
}

$(() => {
  $('input.rut').each((i, rutInput) => {
    new RutInput($(rutInput));
  });
});
