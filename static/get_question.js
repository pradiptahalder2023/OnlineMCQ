const totq = document.getElementById('totalq');
const selAll = document.getElementById('selectAll');


function toggleAllCheckboxes(source) {
    let checkboxes = document.getElementsByClassName('form-check-input'); // Or document.getElementsByName('item');
    for (let i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = source.checked;
    }
}

// function to check total no of question selected
function countCheckedCheckboxes() {
  // Select all input elements with type="checkbox" that are currently checked
  const checkedCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');

  // The 'length' property of the NodeList will give you the count
  let count = checkedCheckboxes.length;

  totq.innerText = selAll.checked ? count - 1 : count;
  // return count;
}

document.addEventListener('DOMContentLoaded', () => {
  const checkboxes = document.querySelectorAll('input[type="checkbox"]');
  checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', countCheckedCheckboxes);
  });
  // Initial count on page load
  countCheckedCheckboxes();
});


// final.addEventListener('click', function (e) {
//     e.preventDefault();
     
//     const selectedQuestions = [];
//     for (let i = 0; i < questionOptions.length; i++) {
//         if (questionOptions[i].checked) {
//             selectedQuestions.push(questionOptions[i].value); 
//         }
//     }
//     console.log("Selected Question options:", selectedQuestions);

//     const data = selectedQuestions;
//     console.log("Data sent:", data);

//     fetch('/process-data', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ data: data })
//     })
//         .then(response => response.text())
//         .then(result => {
//             console.log(result);
//         })
//         .catch(error => {
//             console.error('Error:', error);
//         });
// })