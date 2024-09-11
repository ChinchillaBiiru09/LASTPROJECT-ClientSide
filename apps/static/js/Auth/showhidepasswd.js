// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
// .......................   TAB FORM SIGN UP    .......................
const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#password');
const repassword = document.querySelector('#retype_password');
const currpassword = document.querySelector('#current_password');

togglePassword.addEventListener('change', function (e) {
    // Toggle the type attribute
    const type = currpassword.getAttribute('type') === 'password' ? 'text' : 'password';
    currpassword.setAttribute('type', type);

    const type2 = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type2);
    
    const type3 = repassword.getAttribute('type') === 'password' ? 'text' : 'password';
    repassword.setAttribute('type', type3);
    
    // Toggle the checkbox label
    this.nextElementSibling.textContent = type === 'password' ? ' Show Password' : ' Hide Password';
});
// ......................   END TAB FORM SIGN UP   .....................
// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>