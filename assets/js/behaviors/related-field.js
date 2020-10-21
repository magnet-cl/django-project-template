$(document).ready(() => {
  const openUpdateFormBtnSelector = '.open-related-field-update-form';
  const openCreateFormBtnSelector = '.open-related-field-create-form';
  const relatedFieldContainerSelector = '.related-field';
  let win;
  let $select;

  function closeWindow(newID, newRepr) {
    if (win) {
      if (newID) {
        $select.append(
          `<option value="${newID}" selected>${newRepr}</option>`
        );
      }
      win.close();
      win = undefined;
      $select = undefined;
    }
  }

  function openCreateFormBtnClicked() {
    const $this = $(this);
    let url = $this.data('url');

    if (url.indexOf('?') === -1) {
      url += '?popup=1';
    } else {
      url += '&popup=1';
    }

    $select = $this.closest(relatedFieldContainerSelector).find('select');
    closeWindow();
    win = window.open(
      url,
      'Create',
      'height=500,width=800,resizable=yes,scrollbars=yes'
    );
    win.focus();
  }

  function openUpdateFormBtnClicked() {
    const $this = $(this);
    let url = $this.data('url');

    $select = $this.closest(relatedFieldContainerSelector).find('select');

    if (!$select.val()) {
      return;
    }

    url = url.replace('__fk__', $select.val());

    if (url.indexOf('?') === -1) {
      url += '?popup=1';
    } else {
      url += '&popup=1';
    }

    closeWindow();
    win = window.open(
      url,
      'Update',
      'height=500,width=800,resizable=yes,scrollbars=yes'
    );
    win.focus();

    // $.showModal({title: "Hello World!", body: "A very simple modal dialog without buttons."});
  }

  $(openCreateFormBtnSelector).click(openCreateFormBtnClicked);
  $(openUpdateFormBtnSelector).click(openUpdateFormBtnClicked);

  window.closeWindow = closeWindow;

  window.addEventListener('beforeunload', () => {
    closeWindow();
  }, false);
});
