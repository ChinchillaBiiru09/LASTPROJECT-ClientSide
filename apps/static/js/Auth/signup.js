// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
// .......................   TAB FORM SIGN UP    .......................
const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#password');
const repassword = document.querySelector('#retype_password');

togglePassword.addEventListener('change', function (e) {
    // Toggle the type attribute
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    
    const type2 = repassword.getAttribute('type') === 'password' ? 'text' : 'password';
    repassword.setAttribute('type', type2);
    
    // Toggle the checkbox label
    this.nextElementSibling.textContent = type === 'password' ? ' Show Password' : ' Hide Password';
});
// ......................   END TAB FORM SIGN UP   .....................
// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>