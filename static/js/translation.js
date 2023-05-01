function switchLanguage(lang) {
    let xhr = new XMLHttpRequest()
    const fd = new FormData()
    console.log("here")
    fd.set('lang', lang)
    xhr.open('POST', '/switch_lang', true)
    xhr.send(fd)

    // set animation after email send / error notification for registered email
    xhr.onload = function() {
        location.reload()
    }
}


const langSwitcher = document.getElementById('langSwitcher');
function loadLanguage() {
  let xhr = new XMLHttpRequest();
  xhr.open('POST', '/get_lang', true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onload = function() {
    if (xhr.status === 200) {
      let response = JSON.parse(xhr.responseText);
      let lang = response.lang;
      langSwitcher.value = lang;
    } else {
      console.log('Error getting language');
    }
  };
  xhr.send();
}

loadLanguage()