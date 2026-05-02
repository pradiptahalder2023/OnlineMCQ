const vquestion = document.getElementById('vquestion');
const vop1 = document.getElementById('vop1');
const vop2 = document.getElementById('vop2');
const vop3 = document.getElementById('vop3');
const vop4 = document.getElementById('vop4');
const vanswer = document.getElementById('vanswer');


vquestion.addEventListener('click',(e)=>{
e.preventDefault();
const qquestion = document.getElementById('qquestion');
fetchvoiceapi(qquestion);
});

vop1.addEventListener('click',(e)=>{
e.preventDefault();
const qop1 = document.getElementById('qop1');
fetchvoiceapi(qop1);
});

vop2.addEventListener('click',(e)=>{
e.preventDefault();
const qop2 = document.getElementById('qop2');
fetchvoiceapi(qop2);
});

vop3.addEventListener('click',(e)=>{
e.preventDefault();
const qop3 = document.getElementById('qop3');
fetchvoiceapi(qop3);
});

vop4.addEventListener('click',(e)=>{
e.preventDefault();
const qop4 = document.getElementById('qop4');
fetchvoiceapi(qop4);
});

vanswer.addEventListener('click',(e)=>{
e.preventDefault();
const qanswer = document.getElementById('qanswer');
fetchvoiceapi(qanswer);
});



// on load of the form
document.addEventListener('DOMContentLoaded', function () {

  // sets the value in class select box
  document.getElementById('qclass').value = receivedData[0].studyclass;

  // sets the value in semesters select box
  document.getElementById('qsem').value = receivedData[0].sem;

   // sets the value in chapter select box
  document.getElementById('qchapter').value = receivedData[0].chapter;

   // sets the value in qtype select box
  document.getElementById('qtype').value = receivedData[0].Question_Type_id;

  // sets the value in hasimage select box
  document.getElementById('qhasimage').value = receivedData[0].hasimage;

  // sets the value in imagefile select box
  document.getElementById('qfilename').value = receivedData[0].imagelocation;
  

  // sets the value in question input box
  document.getElementById('qquestion').value = receivedData[0].question;

  // sets the value in option1 input box
  document.getElementById('qop1').value = receivedData[0].op1;

  // sets the value in option2 input box
  document.getElementById('qop2').value = receivedData[0].op2;

  // sets the value in option3 input box
  document.getElementById('qop3').value = receivedData[0].op3;

  // sets the value in option4 input box
  document.getElementById('qop4').value = receivedData[0].op4;

  // sets the value in answer input box
  document.getElementById('qanswer').value = receivedData[0].answer;



  // Get the field element by its ID
  var selectElement = document.getElementById("qhasimage");
  var inputElement = document.getElementById("qimagefile");
  var filenameElement = document.getElementById("qfilename");

  // Check if the field exists and then enable it
  if (selectElement.value === "No") {
    inputElement.disabled = true
    filenameElement.style.display='none'
  } else {
    inputElement.disabled = false
    filenameElement.style.display='block'
    filenameElement.readOnly=true
    if (receivedData[0].imagelocation !== ""){
      filenameElement.value = receivedData[0].imagelocation
    }  
  }

});

// enable or disable imagefile input field on change of qhasimage
function toggleInput() {
  var selectElement = document.getElementById("qhasimage");
  var inputElement = document.getElementById("qimagefile");
  var filenameElement = document.getElementById("qfilename");

  if (selectElement.value === "No") {
    inputElement.disabled = true
    filenameElement.style.display='none'
  } else {
    inputElement.disabled = false
    filenameElement.style.display='block'
    filenameElement.readOnly=true
    if (receivedData[0].imagelocation !== ""){
      filenameElement.value = receivedData[0].imagelocation
    }  
  }
}


// function that actually does the speech recognition
function fetchvoiceapi(element) {
    fetch('/voice')
    .then(response => response.json())
    .then(data => {
      //dynamically select input field for voice inputted text
      setTextToCurrentPos(element, data.vdata)
    })
    .catch(error => console.error('Error fetching data:', error));
}

//function to insert inputted voice text at currenr cursor posion
function setTextToCurrentPos(element, insert) {
  var curPos = element.selectionStart;
  let x = element.value;
  let text_to_insert = insert;
  element.value = x.slice(0, curPos) + text_to_insert + " " + x.slice(curPos);
}



