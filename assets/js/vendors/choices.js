// Vendors
import Choices from 'choices.js';

// Constants
const CHOICES_LANG_TEXTS = {
  en: {
    loadingText: 'Loading...',
    noResultsText: 'No results found',
    noChoicesText: 'No choices to choose from',
    itemSelectText: '',
    addItemText: (value) => `Press Enter to add <b>"${value}"</b>`,
    maxItemText: (maxItemCount) => `Only ${maxItemCount} values can be added`
  },
  es: {
    loadingText: 'Cargando...',
    noResultsText: 'No se encontraron resultados',
    noChoicesText: 'No hay opciones para elegir',
    itemSelectText: '',
    addItemText: (value) => `Pressione Enter para agregar <b>"${value}"</b>`,
    maxItemText: (maxItemCount) => `Sólo se pueden agregar ${maxItemCount} valores`
  }
};

// Functions
/**
 * Define if the placeholder should is visible to the user or not.
 * If `choices` has selected options, then hide it. Otherwise, show it.
 * @param {Choices} choices
 */
function setChoicesMultiplePlaceholderVisibility(choices) {
  const searchInput = choices.input.element;
  const hasSelectedOptions = choices.getValue().length !== 0;

  if (hasSelectedOptions) {
    searchInput.classList.add('choices__input--placeholder-hidden');
  } else {
    searchInput.classList.remove('choices__input--placeholder-hidden');
  }
}

/**
 * Initialize `select` element as a Choices
 * @param {HTMLSelectElement} select
 * @returns {Choices}
 */
export function initChoices(select) {
  const documentLang = document.documentElement.lang;
  const isMultiple = select.hasAttribute('multiple');
  const placeholder = select.querySelector('option[value=""]')?.textContent;
  const options = {
    shouldSort: false,
    searchResultLimit: 100,
    removeItemButton: isMultiple,
    placeholderValue: '',
    allowHTML: false,
    ...CHOICES_LANG_TEXTS[documentLang]
  };
  const choices = new Choices(select, options);

  // Hide placeholder if select has selected options
  if (isMultiple && placeholder) {
    setChoicesMultiplePlaceholderVisibility(choices);
    select.addEventListener('change', () => {
      setChoicesMultiplePlaceholderVisibility(choices);
    }, false);
  }

  return choices;
}

// Initialize behavior
window.addEventListener('DOMContentLoaded', () => {
  const choicesSelects = document.querySelectorAll('select:not(.js-not-choices):not(#id_region):not(#id_commune)');

  choicesSelects.forEach(initChoices);
});
