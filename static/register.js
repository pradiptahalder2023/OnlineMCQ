$(document).ready(function () {
  setTimeout(function () {
    $('.alert').alert('close');
  }, 3000); // 2000 milliseconds = 3 seconds
});


// password show / hide
const passwordInput = document.getElementById('password');
const toggleButton = document.getElementById('togglePassword');

const confirmpasswordInput = document.getElementById('confirmpassword');
const confirmtoggleButton = document.getElementById('confirmtogglePassword');


toggleButton.addEventListener('click', function () {
  if (passwordInput.getAttribute('type') === 'password') {
    passwordInput.setAttribute('type', 'text');
    this.classList.remove('fa-eye');
    this.classList.add('fa-eye-slash');
  }
  else{
    passwordInput.setAttribute('type', 'password');
    this.classList.remove('fa-eye-slash');
    this.classList.add('fa-eye');
  }
});

confirmtoggleButton.addEventListener('click', function () {
  if (confirmpasswordInput.getAttribute('type') === 'password') {
    confirmpasswordInput.setAttribute('type', 'text');
    this.classList.remove('fa-eye');
    this.classList.add('fa-eye-slash');
  }
  else{
    confirmpasswordInput.setAttribute('type', 'password');
    this.classList.remove('fa-eye-slash');
    this.classList.add('fa-eye');
  }
  });
