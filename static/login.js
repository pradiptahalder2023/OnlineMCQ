$(document).ready(function () {
  setTimeout(function () {
    $('.alert').alert('close');
  }, 3000); // 2000 milliseconds = 3 seconds
});


// password show / hide
const passwordInput = document.getElementById('password');
const toggleButton = document.getElementById('togglePassword');

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
