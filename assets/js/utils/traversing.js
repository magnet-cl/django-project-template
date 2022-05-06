/**
 * Get the `elem`'s closest parent that matches `selector`.
 * Returns `null` if there isn't any.
 * @param {HTMLElement} elem
 * @param {DOMString} selector
 * @returns {HTMLElement|null}
 */
export function getParentBySelector(elem, selector) {
  // eslint-disable-next-line no-param-reassign
  for (; elem && elem !== document; elem = elem.parentNode) {
    if (elem.matches(selector)) {
      return elem;
    }
  }

  return null;
}
