const wrapper = document.querySelector('.wrapper');
const signUpLink = document.querySelector('.signUp-link');
const signInLink = document.querySelector('.signIn-link');
const staffInLink = document.querySelector('.staffSignIn-link');
const customerInLink = document.querySelector('.customerSignIn-link');
const forgetPasswordLink = document.querySelector('.forgetpassword-link');
const gobackLink = document.querySelector('.goback-link');

// boolean value that represent each input is valid
let validUserName = false, validPassword = false, validRePassword = false, validEmail = false

// input area
const email_input = document.getElementById('signup-email');
const username_input = document.getElementById("signup-username")
const password_input = document.getElementById("signup-password")
const repassword_input = document.getElementById("signup-confirm-password")
const captcha_input = document.getElementById("signup-captcha")

// text area
const email_error = document.getElementById('email_error');
const username_error = document.getElementById("username_error");
const captcha_error = document.getElementById("captcha_error");
const password_error = document.getElementById("password_error");
const repassword_error = document.getElementById("Repassword_error");

// login area
const login_email = document.getElementById('signin-email');
const login_password = document.getElementById('signin-password');

// count down
const num_div = document.getElementById('register-count')

signUpLink.addEventListener('click', () => {
    // if (wrapper.classList.contains('animate-staffIn')){
    //     wrapper.classList.remove('animate-staffIn');
    // }
    if (wrapper.classList.contains('animate-goback')){
        wrapper.classList.remove('animate-goback');
    }
    wrapper.classList.add('animate-signIn');
    wrapper.classList.remove('animate-signUp');
});

signInLink.addEventListener('click', () => {
    wrapper.classList.add('animate-signUp');
    wrapper.classList.remove('animate-signIn');
});

// staffInLink.addEventListener('click', () => {
//     if (wrapper.classList.contains('animate-goback')){
//         wrapper.classList.remove('animate-goback');
//     }
//     wrapper.classList.add('animate-signIn2');
//     wrapper.classList.remove('animate-staffIn');
// })

// customerInLink.addEventListener('click', () => {
//     wrapper.classList.add('animate-staffIn');
//     wrapper.classList.remove('animate-signIn2');
// })

forgetPasswordLink.addEventListener('click', () => {
    // if (wrapper.classList.contains('animate-staffIn')){
    //     wrapper.classList.remove('animate-staffIn');
    // }
    if (wrapper.classList.contains('animate-signUp')){
        wrapper.classList.remove('animate-signUp');
    }
    wrapper.classList.add('animate-forget');
    wrapper.classList.remove('animate-goback');
})

gobackLink.addEventListener('click', () => {
    wrapper.classList.add('animate-goback');
    wrapper.classList.remove('animate-forget');
})

// send email
function send_email(){
    // check if is empty
    let email = email_input.value
    if (email === '') {
        email_error.innerHTML = "empty email"
        return;
    }
    // check if is wrong format
    if (!validEmail) {
        email_error.innerHTML = "invalid email format"
        return;
    }

    // animation when the email is sent
    countDown(60, num_div).then(r => {})

    // send email
    let xhr = new XMLHttpRequest()
    const fd = new FormData()
    fd.set('email', document.getElementById('signup-email').value)
    xhr.open('POST', '/captcha', true)
    xhr.send(fd)


    // display error messages
    xhr.onload = function() {
        let response = JSON.parse(xhr.responseText)
        if (response.code === 400) {
            email_error.innerHTML = response.message;
        } else if (response.code === 401) {
            let msg = response.message
            alert(msg)
        }
    }
}

// sign up
function SignUp(){
    // check empty
    let flag = true

    if (username_input.value === '') {
        username_error.innerHTML = 'empty user name'
        flag = false;
    }
    if (password_input.value === '') {
        password_error.innerHTML = 'empty password'
        flag = false;
    }
    if (repassword_input.value === '') {
        repassword_error.innerHTML = 'empty password'
        flag = false;
    }
    if (email_input.value === '') {
        email_error.innerHTML = 'empty email'
        flag = false;
    }
    if (captcha_input.value === '') {
        captcha_error.innerHTML = 'empty captcha'
        flag = false;
    }
    if (!flag) return;

    // check data validation:
    if (!validEmail || !validUserName || !validPassword || !validRePassword) {
        return;
    }

    // send registered form to flask backend
    let xhr = new XMLHttpRequest()
    xhr.open('POST', '/register', true)
    xhr.setRequestHeader("X-CSRFToken", "{{ register_form.csrf_token._value() }}")
    let form = document.getElementById("signup-form")
    const fd = new FormData(form)
    xhr.send(fd)

    // display error messages
    xhr.onload = function() {
        let response = JSON.parse(xhr.responseText)
        if (response.code === 400) {
            let msg = response.message
            switch (msg) {
                case 'captcha out of time':
                    captcha_error.innerHTML = msg
                    break
                case 'captcha wrong':
                    captcha_error.innerHTML = msg
                    break
                case 'registered username':
                    username_error.innerHTML = msg
                    break
                case 'registered email':
                    email_error.innerHTML = msg
                    alert("aaaaaaaaaa======")
                    break
                case 'registered user name':
                    username_error.innerHTML = msg
                    break
                case 'email not validate':
                    email_error.innerHTML = msg
                    break
                case 'wrong username format':
                    username_error.innerHTML = msg
                    break
                case 'wrong password format':
                    password_error.innerHTML = msg
                    break
            }
        } else if (response.code === 401) {
            let msg = response.message
            alert(msg)
        } else {
            // go to log in page and load email and password automatically
            wrapper.classList.add('animate-signUp');
            wrapper.classList.remove('animate-signIn');
            // add text automatically
            login_email.value = email_input.value;
            login_password.value = password_input.value;
        }
    }
}

// sign in
function SignIn(){
    let xhr = new XMLHttpRequest()
    xhr.open('POST', '/login', true)
    xhr.setRequestHeader("X-CSRFToken", "{{ login_form.csrf_token._value() }}")
    let form = document.getElementById("signin-form")
    xhr.send(new FormData(form))
    xhr.onload = function() {
        let response = JSON.parse(xhr.responseText)
        if (response.code === 200) {
            console.log(200)
            window.open(response.message,"_self")
        } else {
            alert(response.message)
        }
    }
}

// various listeners for signup page
function username_listener_sign_up() {
    validUserName = username_listener(username_error, username_input);
}

function password_listener_sign_up() {
    validPassword = password_listener(password_input, password_error);
}

function rePassword_listener_sign_up() {
    validRePassword = rePassword_listener(repassword_error, password_input, repassword_input)
}
function email_listener_sign_up() {
    validEmail = email_listener(email_input, email_error);
}
function captcha_listener_sign_up() {
    captcha_error.innerHTML = ""
}

