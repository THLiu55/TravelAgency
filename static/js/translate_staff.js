const langSwitcher = document.getElementById('langSwitcher');

function switchLanguage(lang) {
    let xhr = new XMLHttpRequest()
    const fd = new FormData()
    fd.set('lang', lang)
    xhr.open('POST', '/switch_lang', true)
    xhr.send(fd)

    // set animation after email send / error notification for registered email
    xhr.onload = function() {
        location.reload()
    }
}


function loadLanguage() {
  let xhr = new XMLHttpRequest();
  xhr.open('POST', '/get_lang', true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onload = function() {
    if (xhr.status === 200) {
      let response = JSON.parse(xhr.responseText);
      let lang = response.lang;
      if (lang === "zh") {
          langSwitcher.innerHTML = `<option value="en">{{ _("ENG") }}</option><option value="zh">{{ _("CHN") }}</option>`
      } else {
          langSwitcher.innerHTML = `<option value="zh">{{ _("CHN") }}</option><option value="en">{{ _("ENG") }}</option>`
      }
    } else {
      console.log('Error getting language');
    }
  };
  xhr.send();
}

loadLanguage()