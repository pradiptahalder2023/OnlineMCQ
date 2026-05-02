// password show / hide
const oldpasswordInput = document.getElementById('oldpassword');
const oldtoggleButton = document.getElementById('oldtogglePassword');

const newpasswordInput = document.getElementById('newpassword');
const newtoggleButton = document.getElementById('newtogglePassword');

const confirmnewpasswordInput = document.getElementById('confirmnewpassword');
const confirmnewtoggleButton = document.getElementById('confirmnewtogglePassword');

oldtoggleButton.addEventListener('click', function () {
  if (oldpasswordInput.getAttribute('type') === 'password') {
    oldpasswordInput.setAttribute('type', 'text');
    this.classList.remove('fa-eye');
    this.classList.add('fa-eye-slash');
  }
  else{
    oldpasswordInput.setAttribute('type', 'password');
    this.classList.remove('fa-eye-slash');
    this.classList.add('fa-eye');
  }
});

newtoggleButton.addEventListener('click', function () {
  if (newpasswordInput.getAttribute('type') === 'password') {
    newpasswordInput.setAttribute('type', 'text');
    this.classList.remove('fa-eye');
    this.classList.add('fa-eye-slash');
  }
  else{
    newpasswordInput.setAttribute('type', 'password');
    this.classList.remove('fa-eye-slash');
    this.classList.add('fa-eye');
  }
});

confirmnewtoggleButton.addEventListener('click', function () {
  if (confirmnewpasswordInput.getAttribute('type') === 'password') {
    confirmnewpasswordInput.setAttribute('type', 'text');
    this.classList.remove('fa-eye');
    this.classList.add('fa-eye-slash');
  }
  else{
    confirmnewpasswordInput.setAttribute('type', 'password');
    this.classList.remove('fa-eye-slash');
    this.classList.add('fa-eye');
  }
});
