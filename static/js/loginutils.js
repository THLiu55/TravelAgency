const reg = /^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$/

function checkEmailFormat(email) {
    return reg.test(email)
}

// delay a second
function delay(milliseconds) {
    return new Promise(resolve => {
        setTimeout(resolve, milliseconds);
    });
}

// count Down for seconds (used in sending email)
async function countDown(seconds) {
    const num_div = document.getElementById('count')
    const sending_btn = document.getElementById('register-email-btn')
    sending_btn.disabled = true
    sending_btn.style.backgroundColor = '#67a0ff'
    for (let i = seconds; i > 0; i--) {
        num_div.innerHTML = i.toString()
        await delay(1000)
    }
    sending_btn.disabled = false
    sending_btn.style.backgroundColor = '#1a2886'
    num_div.innerHTML = "SEND";
}

// set input event listeners
function email_listener(email_input, email_error) {
    // clear the error message
    email_error.innerHTML = "";
    // obtain input email
    let email = email_input.value
    // check if the email is in correct format (aaa@bbb.ccc)
    let correct = reg.test(email)
    console.log(email)
    if (correct) {
        return true
    }
    if (email !== '') {
        email_error.innerHTML = "incorrect format"
    } else {
        email_error.innerHTML = "empty"
    }
}

function username_listener(username_error, username_input) {
    // clear error message
    username_error.innerHTML = "";
    // obtain username
    let username = username_input.value
    // check if username is valid (3 < length < 20)
    if (username.length >= 3 && username.length <= 20) {
        return true;
    }
    if (username.length === 0) {
        username_error.innerHTML = "empty"
        return false;
    }
    if (username.length < 3) {
        username_error.innerHTML = "too short"
        return false
    }
    if (username.length > 20) {
        username_error.innerHTML = "too long"
    }
    return false
}

function captcha_listener(captcha_input, captcha_error) {
    captcha_error.innerHTML = "";
    // obtain captcha
    let captcha = captcha_input.value
    // check if captcha is valid (int(0-9) * 6)
    for (let i = 0; i < captcha.length; i++) {
        if (i === 6 || captcha[i] < '0' || captcha[i] > '9') {
            captcha_error.innerHTML = "wrong captcha";
            return false;
        }
    }
    return true
}

function password_listener(password_input, password_error) {
    // get password
    password_error.innerHTML = ""
    let hasLetter = false, hasNum = false, hasCap = false
    let password = password_input.value
    let len = password.length

    // check length
    if (len < 6) {
        password_error.innerHTML = "too short"
        return false
    }
    if (len > 20) {
        password_error.innerHTML = "too long"
        return false
    }

    // check format
    for (let i = 0; i < password.length; i++) {
        if ('0' <= password[i] && password[i] <= '9') {
            hasNum = true
        } else if (('a' <= password[i] && password[i] <= 'z') || ('A' <= password[i] && password[i] <= 'Z')) {
            hasLetter = true
            if ('A' <= password[i] && password[i] <= 'Z') {
                hasCap = true
            }
        }
        // if all satisfied -> return
        if (hasNum && hasLetter && hasCap && 6 <= len && len <= 20) {
            return true
        }
    }
    // show error message and set valid to false
    if (!hasLetter) {
        password_error.innerHTML = "weak (need letters)"
        return false;
    }
    if (!hasNum) {
        password_error.innerHTML = "weak (need number)"
        return false;
    }
    if (!hasCap) {
        password_error.innerHTML = "weak (need capital letter)"
    }
    return false
}

// check if re-input password == password
function rePassword_listener(repassword_error, password_input, repassword_input) {
    // clear error message
    repassword_error.innerHTML = ""
    let pass = password_input.value
    let repass = repassword_input.value
    if (pass != repass) {
        repassword_error.innerHTML = "password not match"
        return false;
    }
    return true
}