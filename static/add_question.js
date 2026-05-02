const vquestion = document.getElementById('vquestion');
const vop1 = document.getElementById('vop1');
const vop2 = document.getElementById('vop2');
const vop3 = document.getElementById('vop3');
const vop4 = document.getElementById('vop4');
const vanswer = document.getElementById('vanswer');

const vLangquestion = document.getElementById('vLangquestion');
const vLangop1 = document.getElementById('vLangop1');
const vLangop2 = document.getElementById('vLangop2');
const vLangop3 = document.getElementById('vLangop3');
const vLangop4 = document.getElementById('vLangop4');
const vLanganswer = document.getElementById('vLanganswer');


const qclass = document.getElementById('qclass');
const qsem = document.getElementById('qsem');
const qchapter = document.getElementById('qchapter');
const qtype = document.getElementById('qtype');

var selectElement = document.getElementById("qhasimage");
var inputElement = document.getElementById("qimagefile");
// var filenameElement = document.getElementById("qfilename");


//vkeyboard
var keyboardContainer = null;
var textarea = null;
var keyboardLayout = []
var kbLayout = []
shifted = false

// on load of the form
document.addEventListener('DOMContentLoaded', function () {

  //sets imagefile operative/readonly
  toggleInput();

  // Retrieve and set the select option value on page load (from localstorage):
  const savedValue_qclass = localStorage.getItem("qclass");
  // console.log(savedValue_qclass);
  if (savedValue_qclass) {
    qclass.value = savedValue_qclass;
  }

  const savedValue_qsem = localStorage.getItem("qsem");
  if (savedValue_qsem) {
    qsem.value = savedValue_qsem;
  }

  const savedValue_qchapter = localStorage.getItem("qchapter");
  if (savedValue_qchapter) {
    qchapter.value = savedValue_qchapter;
  }

  const savedValue_qtype = localStorage.getItem("qtype");
  // console.log(savedValue_qtype);
  if (savedValue_qtype) {
    qtype.value = savedValue_qtype;
  }
});


// section that retains select options accross page submit / refresh (localstorage)
qclass.addEventListener("change", function () {
  localStorage.setItem("qclass", this.value);
})
qsem.addEventListener("change", function () {
  localStorage.setItem("qsem", this.value);
})
qchapter.addEventListener("change", function () {
  localStorage.setItem("qchapter", this.value);
})
qtype.addEventListener("change", function () {
  localStorage.setItem("qtype", this.value);

  //displays modal if column matching question type is selected
  const selectedIndex = this.selectedIndex;
  const selectedOptionText = this.options[selectedIndex].text;
  // console.log(selectedOptionText)
  if (selectedOptionText == 'Match the columns') {
    showMyModal();
  }

  //displays modal if Drag and Drop question type is selected
  if (selectedOptionText == 'Drag and Drop Type') {
    showMyModal2();
  }
})

//function to show the modal (for column matching question type)
function showMyModal() {
  $('#myModal').modal('show'); // Shows the modal
}

//function to show the modal (for Drag and Drop question type)
function showMyModal2() {
  $('#myModal2').modal('show'); // Shows the modal
}


// section for voice recognition and prevents auto refresh or auto submit
vquestion.addEventListener('click', (e) => {
  e.preventDefault();
  const qquestion = document.getElementById('qquestion');
  fetchvoiceapi(qquestion);
});

vop1.addEventListener('click', (e) => {
  e.preventDefault();
  const qop1 = document.getElementById('qop1');
  fetchvoiceapi(qop1);
});

vop2.addEventListener('click', (e) => {
  e.preventDefault();
  const qop2 = document.getElementById('qop2')
  fetchvoiceapi(qop2);
});

vop3.addEventListener('click', (e) => {
  e.preventDefault();
  const qop3 = document.getElementById('qop3');
  fetchvoiceapi(qop3);
});

vop4.addEventListener('click', (e) => {
  e.preventDefault();
  const qop4 = document.getElementById('qop4');
  fetchvoiceapi(qop4);
});

vanswer.addEventListener('click', (e) => {
  e.preventDefault();
  const qanswer = document.getElementById('qanswer');
  fetchvoiceapi(qanswer);
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



// enable or disable imagefile input field on change of selection on the form

selectElement.addEventListener('change', function () {
  toggleInput();
})

// enable or disable imagefile input field on change of qhasimage
function toggleInput() {
  var selectElement = document.getElementById("qhasimage");
  var inputElement = document.getElementById("qimagefile");

  if (selectElement.value === "No") {
    inputElement.disabled = true
  } else {
    inputElement.disabled = false
  }
}


// enable or disable virtual keyboard
function onCliclDisplayKeyboard(e, element, textBoxName) {
  e.preventDefault(); //disables auto page refreshing
  const myElement = document.querySelector('.container-virtual-keyboard');

  if (myElement) {
    // keyboard exists and remove it
    removeElementsByClass('container-virtual-keyboard');

  } else {
    // Element does not exist and create keyboard

    //clears the previous layout
    keyboardLayout = [];
    kbLayout = [];

    const selATag = document.getElementById(element.id);
    parent = selATag.parentElement;

    const newDiv = document.createElement('div');
    newDiv.classList.add('container-virtual-keyboard');

    const anothernewDiv = document.createElement('div');
    // for big and small testbox, use different class
    if (textBoxName === 'qquestion') {
      anothernewDiv.id = "virtual-keyboard-large";
    }
    else {
      anothernewDiv.id = "virtual-keyboard-small";
    }

    newDiv.appendChild(anothernewDiv);
    parent.appendChild(newDiv);

    textarea = document.getElementById(textBoxName);
    if (textBoxName === 'qquestion') {
      keyboardContainer = document.getElementById('virtual-keyboard-large');
    }
    else {
      keyboardContainer = document.getElementById('virtual-keyboard-small');
    }

    // Convert unicode to character
    unicodeToChar(normalKeyboardLayoutUnicode);
    console.log(keyboardLayout)
    // Initialize the keyboard when the page loads
    createKeyboard();
  }
}

function removeElementsByClass(className) {
  const elements = document.getElementsByClassName(className);
  while (elements.length > 0) {
    elements[0].parentNode.removeChild(elements[0]);
  }
}



const normalKeyboardLayoutUnicode = [
  //অ    ই     উ     ঋ    এ     ও    ক     গ    ঙ     চ   
  [2437, 2439, 2441, 2443, 2447, 2451, 2453, 2455, 2457, 2458],
  //জ    ঞ    ট     ড     ণ     ত    দ     প     ব    ম
  [2460, 2462, 2463, 2465, 2467, 2468, 2470, 2474, 2476, 2478],
  //য     র     ল     শ    স     ড়    'া'   'ি'   'ু'   'ে'
  [2479, 2480, 2482, 2486, 2488, 2524, 2494, 2495, 2497, 2503],
  //'ৈ'   '্'   'ৃ'    ০    ১     ২     ৩    ৪     ৫     ৬   
  [2504, 2509, 2499, 2534, 2535, 2536, 2537, 2538, 2539, 2540],
  //৭     ৮     ৯     ⇧    ⌫  space
  [2541, 2542, 2543, 8679, 9003, 32,],
];

const shiftedKeyboardLayoutUnicode = [
  //আ    ঈ     ঊ    ৎ     ঐ    ঔ    খ     ঘ     'ং   ছ
  [2438, 2440, 2442, 2510, 2448, 2452, 2454, 2456, 2434, 2459],
  //ঝ    'ঃ'    ঠ    ঢ     ন    থ     ধ     ফ     ভ    'ঁ'
  [2461, 2435, 2464, 2466, 2472, 2469, 2471, 2475, 2477, 2433],
  //য়     ।    ?    ষ     হ     ঢ়    ,    'ী'   'ূ'  'ো'  
  [2527, 2404, 63, 2487, 2489, 2525, 44, 2496, 2498, 2507],
  //'ৌ'  :   ;     ০    ১     ২     ৩    ৪     ৫     ৬
  [2508, 58, 59, 2534, 2535, 2536, 2537, 2538, 2539, 2540],
  //৭     ৮     ৯     ⇧    ⌫  space
  [2541, 2542, 2543, 8679, 9003, 32,],

];

// function to convert unicode to character
function unicodeToChar(kbLayout) {
  kbLayout.forEach(row => {
    encode(row);
  });
}

const encode = (list) => {
  const arr = []
  for (let i = 0; i < list.length; i++) {
    let a = String.fromCharCode(list[i]);
    arr.push(a);
  }
  keyboardLayout.push(arr);
}

// function that designs actual keyboard layout
function createKeyboard() {
  // textarea = document.getElementById();
  keyboardLayout.forEach(row => {
    row.forEach(key => {
      const keyElement = document.createElement('div');
      keyElement.classList.add('key');
      keyElement.textContent = key;

      if (key === String.fromCharCode('8679')) {
        keyElement.classList.add('special-key', 'shiftKey');
      }
      else if (key === String.fromCharCode('9003')) {
        keyElement.classList.add('special-key', 'backspaceKey');
      }
      else if (key === String.fromCharCode('32')) {
        keyElement.classList.add('special-key', 'spacebarKey');
      }


      keyElement.addEventListener('click', () => {
        handleKeyClick(key);
      });
      keyboardContainer.appendChild(keyElement);
    });
  });
}

function handleKeyClick(key) {
  if (key === String.fromCharCode('9003')) {
    textarea.value = textarea.value.slice(0, -1);
  } else if (key === String.fromCharCode('32')) {
    textarea.value += ' ';
  } else if (key === String.fromCharCode('8679')) {
    // You would need a more advanced layout and logic for shift functionality
    if (shifted == false) {
      keyboardLayout = []
      kbLayout = []
      keyboardContainer.innerHTML = "";
      // Convert unicode to character
      unicodeToChar(shiftedKeyboardLayoutUnicode);
      // Initialize the keyboard when the page loads
      createKeyboard();
      shifted = true;
      return;
    }
    if (shifted == true) {
      keyboardLayout = []
      kbLayout = []
      keyboardContainer.innerHTML = "";
      // Convert unicode to character
      unicodeToChar(normalKeyboardLayoutUnicode);
      // Initialize the keyboard when the page loads
      createKeyboard();
      shifted = false;
      return;
    }

  } else {
    textarea.value += key;
  }
  textarea.focus();
}

//sets voice language through AJAX request
vLangquestion.addEventListener('change', function () {
  if (this.checked) {
    changeVoiceLanguage('BENG')
  } else {
    changeVoiceLanguage('ENG');
  }
});
vLangop1.addEventListener('change', function () {
  if (this.checked) {
    changeVoiceLanguage('BENG')
  } else {
    changeVoiceLanguage('ENG');
  }
});
vLangop2.addEventListener('change', function () {
  if (this.checked) {
    changeVoiceLanguage('BENG')
  } else {
    changeVoiceLanguage('ENG');
  }
});
vLangop3.addEventListener('change', function () {
   if (this.checked) {
    changeVoiceLanguage('BENG')
  } else {
    changeVoiceLanguage('ENG');
  }
});
vLangop4.addEventListener('change', function () {
  if (this.checked) {
    changeVoiceLanguage('BENG')
  } else {
    changeVoiceLanguage('ENG');
  }
});
vLanganswer.addEventListener('change', function () {
  if (this.checked) {
    changeVoiceLanguage('BENG')
  } else {
    changeVoiceLanguage('ENG');
  }
});


function changeVoiceLanguage(voiceLang) {
  const inputValue = voiceLang;

  fetch('/change_voice_language', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ value: inputValue })
  })
    .then(response => response.json())
    .then(data => {
      // console.log(data.message);
      // Optionally, update the UI based on the server response
    })
    .catch(error => {
      console.error('Error:', error);
    });
}