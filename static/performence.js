document.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('.tab');
  const panels = document.querySelectorAll('.tab-panel');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      // Deactivate current active tab and panel
      document.querySelector('.tab.active').classList.remove('active');
      document.querySelector('.tab-panel.active').classList.remove('active');

      // Activate clicked tab and its corresponding panel
      tab.classList.add('active');
      const targetPanelId = tab.dataset.tab;
      document.getElementById(targetPanelId).classList.add('active');
    });
  });
});

$(document).ready(function() {
    $('#myTable').DataTable();
});