const wrapper = document.querySelector('.wrapper')
const LoginLink = document.querySelector('.Login-link')
const registerLink = document.querySelector('.register-link')
const btnPopup = document.querySelector('.btnLogin-popup')

registerLink.addEventListener('click',()=>{
    wrapper.classList.add('active');
})

LoginLink.addEventListener('click',()=>{
    wrapper.classList.add('active');
})

btnPopup.addEventListener('click',()=>{
    wrapper.classList.add('active');
});
iconClose.addEventListener('click',()=>{
    wrapper.classList.remove('active-popup');
});