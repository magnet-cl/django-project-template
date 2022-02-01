// Vendors
import axios from 'axios';
import { initChoices } from '../vendors/choices';

// Constants
const REGION_SELECT_SELECTOR = '#id_region';
const COMMUNE_SELECT_SELECTOR = '#id_commune';

// Functions
/**
 * Gets the list of communes corresponding to the region with `id` equals to `regionId`.
 * @param {String|Number} regionId
 * @returns {Array}
 */
async function getRegionCommunes(regionId) {
  try {
    const regionIdIsInteger = /^\d+$/.test(regionId);

    if (!regionIdIsInteger) {
      throw new Error('regionId is not a positive integer.');
    }

    const communes = await axios.get('/regions/communes/search/', {
      params: { regionId }
    });

    return communes.data;
  } catch {
    return [];
  }
}

/**
 * Replaces the list of communes of `communeChoices`.
 * @param {Choices} communeChoices
 * @param {String|Number} regionId
 * @returns {void}
 */
async function setCommuneOptions(communeChoices, regionId) {
  const communes = await getRegionCommunes(regionId);

  const communeSelect = communeChoices.passedElement.element;
  const communeSelectPlaceholder = communeSelect.dataset.placeholder;

  if (communeSelectPlaceholder) {
    communes.unshift({
      id: '',
      text: communeSelectPlaceholder,
      selected: true
    });
  }

  communeChoices.setChoices(communes, 'id', 'text', true);
}

// Initialize behavior
window.addEventListener('DOMContentLoaded', () => {
  // Init choices
  const regionSelect = document.querySelector(REGION_SELECT_SELECTOR);
  const communeSelect = document.querySelector(COMMUNE_SELECT_SELECTOR);

  if (!regionSelect || !communeSelect) return;

  const regionChoices = initChoices(regionSelect);
  const communeSelectPlaceholder = communeSelect.querySelector('option[value=""]')?.textContent;
  const communeChoices = initChoices(communeSelect);

  // Store placeholder as data attribute
  communeSelect.dataset.placeholder = communeSelectPlaceholder;

  // Add initial commune options
  setCommuneOptions(communeChoices, regionChoices.getValue(true));

  // Update commune options whenever the region changes
  regionSelect.addEventListener('change', (choice) => {
    const regionId = choice.detail.value;

    setCommuneOptions(communeChoices, regionId);
  });
});
