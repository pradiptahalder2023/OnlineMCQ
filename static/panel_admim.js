const sidebar = document.getElementById('sidebar')

//  document.addEventListener('DOMContentLoaded', function() {
//     setTimeout(function() {
//       var alertElement = document.querySelector('.alert');
//       if (alertElement) {
//         var bsAlert = bootstrap.Alert.getOrCreateInstance(alertElement);
//         bsAlert.close();
//       }
//     }, 3000); // 3000 milliseconds = 3 seconds
//   });

$(document).ready(function() {
    setTimeout(function() {
      $('.alert').alert('close');
    }, 3000); // 2000 milliseconds = 3 seconds
  });

  function toggleSidebar(){
    sidebar.classList.toggle('show')
}