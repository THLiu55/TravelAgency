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
