window.onload = () => {
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i += 1) {
        const cookie = cookies[i].trim();

        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (`${name}=`)) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }

    return cookieValue;
  }

  const cookie = getCookie('csrftoken');

  const interval = setInterval(() => {
    if (cookie !== getCookie('csrftoken')) {
      clearInterval(interval);

      const next = document.getElementById('id_next');

      if (next) {
        window.location.href = next.value;
        return;
      }

      window.location.reload();
    }
  }, 1000);


  const loginForm = document.getElementById('login-form');
  const loginField = document.getElementById(loginForm.dataset.usernameFieldId);
  if (loginField) {
    loginField.focus();
    loginField.select();
  }
};
