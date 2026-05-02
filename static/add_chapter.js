const vdesc = document.getElementById('vdesc');

vdesc.addEventListener('click',(e)=>{
e.preventDefault();
const chdesc = document.getElementById('chdesc');
fetchvoiceapi(chdesc);
});

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
