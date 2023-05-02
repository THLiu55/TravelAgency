// forget password area input
const forgetpassemail = document.getElementById('forgetpass-email');
const forgetpasscaptcha = document.getElementById('forgetpass-captcha');
const forgetpasspassword = document.getElementById('forgetpass-password');
const forgetpassrepassword = document.getElementById('forgetpass-repassword');

// input error areas
const forget_email_error = document.getElementById('forget_email_error');
const forget_captcha_error = document.getElementById('forget_captcha_error');
const forget_password_error = document.getElementById('forget_password_error');
const forget_Repassword_error = document.getElementById('forget_Repassword_error');

// login input
const signinemail = document.getElementById('signin-email');
const signinpassword = document.getElementById('signin-password');

// forget password count down area
const forget_num_div = document.getElementById('forget-count')

// forget email send
function forget_email_send(){
    // animation when the email is sent
    forgetcountDown(60, forget_num_div).then(r => {})

    // send the captcha to backend
    let xhr = new XMLHttpRequest()
    let fd = new FormData()
    fd.set("email", forgetpassemail.value)
    fd.set("captcha", forgetpasscaptcha.value)
    xhr.open('POST', '/recaptcha', true)
    xhr.send(fd)

    // after the email had been sent
    xhr.onload = function() {
        let response = JSON.parse(xhr.responseText)
        if (response.code === 401){
            forget_email_error.innerHTML = "email does not exist"
        }
    }
}

// reset password
function resetPassword() {
    // clear all error messages
    forget_password_error.innerText = ''
    forget_Repassword_error.innerText = ''

    // check validity
    let correct_password = password_listener(forgetpasspassword, forget_password_error)
    let correct_rePassword = rePassword_listener(forget_Repassword_error, forgetpasspassword, forgetpassrepassword);   if (!(correct_password && correct_rePassword)) {
        return;
    }

    // obtain the password and re-password
    let password = forgetpasspassword.value

    // send the new password to backend and  reset the password
    let xhr = new XMLHttpRequest()
    let fd = new FormData()
    fd.set("email", forgetpassemail.value)
    fd.set("captcha", forgetpasscaptcha.value)
    fd.set("password", password)
    xhr.open('POST', '/user/findPassword', true)
    xhr.send(fd)

    // after password reset operation
    xhr.onload = function() {
        let response = JSON.parse(xhr.responseText)
        if (response.code === 400) {
            // display error message
            forget_captcha_error.innerHTML = response.message
        } else {
            // go back to login
            wrapper.classList.add('animate-goback');
            wrapper.classList.remove('animate-forget');

            // load email and to input area automatically
            signinemail.value = forgetpassemail.value;
            signinpassword.value = forgetpasscaptcha.value;
        }
    }
}

// various input listeners:
function forget_email_listener() {
    email_listener(forgetpassemail, forget_email_error);
}

function  forget_captcha_listener() {
    captcha_listener(forgetpasscaptcha, forget_captcha_error);
}

function forget_password_listener() {
    password_listener(forgetpasspassword, forget_password_error);
}

function forget_re_password_listener() {
    rePassword_listener(forget_Repassword_error, forgetpasspassword, forgetpassrepassword);
}