class RutInput {
  constructor(input) {
    this.input = input;
    this.hasError = false;
    this.errorId = `${this.input.id}RutError`;

    this.#createRutErrorElement();
    this.#setListeners();
  }

  /**
   * Add error element near input
   */
  #createRutErrorElement() {
    const error = `<span id="${this.errorId}" class="invalid-feedback">RUT inválido.</span>`;
    this.input.insertAdjacentHTML('afterend', error);
  }

  /**
   * Add event listeners
   */
  #setListeners() {
    const enableRutFormating = !this.input.classList.contains('js-do-not-format-rut');
    const enableRutValidation = !this.input.classList.contains('js-do-not-validate-rut');

    if (enableRutFormating) {
      this.input.addEventListener('keyup', this.formatRut.bind(this));
      this.input.addEventListener('change', this.formatRut.bind(this));
    }

    if (enableRutValidation) {
      this.input.addEventListener('keyup', this.validateRut.bind(this));
      this.input.addEventListener('change', this.validateRut.bind(this));
    }
  }

  /**
   * Set input value with correct rut format
   */
  formatRut() {
    let rut = this.input.value.replace(/-/g, '');

    if (rut !== '' && rut.length > 1) {
      rut = rut.replace(/\./g, '');

      const digits = rut.slice(0, -1).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
      const dv = rut.slice(-1);

      this.input.value = `${digits}-${dv}`;
    }
  }

  /**
   * Check if input value is a valid rut
   * @return {boolean}
   */
  rutIsValid() {
    const rut = this.input.value
      .replace(/-/g, '')
      .replace(/\./g, '');

    if (rut.length < 2) {
      return false;
    }

    const digits = rut.slice(0, -1);
    const dv = rut.slice(-1).toUpperCase();

    // calculate DV
    let sum = 0;
    let mult = 2;

    for (let i = digits.length - 1; i >= 0; i -= 1) {
      sum += parseInt(rut[i], 10) * mult;
      mult = (mult + 1) % 8 || 2;
    }

    // check DV
    switch (sum % 11) {
      case 1: return dv === 'K';
      case 0: return dv === '0';
      default: return `${11 - (sum % 11)}` === dv;
    }
  }

  /**
   * Show error messagge
   */
  showRutError() {
    if (this.hasError) return;

    const currentAriaDescribedby = this.input.getAttribute('aria-describedby') || '';
    const inputAriaDescribedby = `${this.errorId} ${currentAriaDescribedby}`
      .replace(/^\s+|\s+$/, '');

    this.input.classList.add('is-invalid');
    this.input.setAttribute('aria-describedby', inputAriaDescribedby);
    this.hasError = true;
  }

  /**
   * Hide error messagge
   */
  hideRutError() {
    if (!this.hasError) return;

    const inputAriaDescribedby = this.input.getAttribute('aria-describedby')
      .replace(this.errorId, '')
      .replace(/^\s+|\s+$/, '');

    this.input.classList.remove('is-invalid');
    if (inputAriaDescribedby) {
      this.input.setAttribute('aria-describedby', inputAriaDescribedby);
    } else {
      this.input.removeAttribute('aria-describedby');
    }
    this.hasError = false;
  }

  /**
   * Show error messagge if input value is not a correct rut
   */
  validateRut() {
    if (this.rutIsValid()) {
      this.hideRutError();
    } else {
      this.showRutError();
    }
  }
}

// Initialize behavior
window.addEventListener('DOMContentLoaded', () => {
  const rutInputs = document.querySelectorAll('input.rut');

  rutInputs.forEach((input) => {
    new RutInput(input); // eslint-disable-line no-new
  });
});
