const wrapper = document.querySelector('.wrapper');
const signUpLink = document.querySelector('.signUp-link');
const signInLink = document.querySelector('.signIn-link');
const staffInLink = document.querySelector('.staffSignIn-link');
const customerInLink = document.querySelector('.customerSignIn-link');

signUpLink.addEventListener('click', () => {
    if (wrapper.classList.contains('animate-staffIn')){
        wrapper.classList.remove('animate-staffIn');
    }
    wrapper.classList.add('animate-signIn');
    wrapper.classList.remove('animate-signUp');
});

signInLink.addEventListener('click', () => {
    wrapper.classList.add('animate-signUp');
    wrapper.classList.remove('animate-signIn');
});

staffInLink.addEventListener('click', () => {
    wrapper.classList.add('animate-signIn2');
    wrapper.classList.remove('animate-staffIn');
})

customerInLink.addEventListener('click', () => {
    wrapper.classList.add('animate-staffIn');
    wrapper.classList.remove('animate-signIn2');
})