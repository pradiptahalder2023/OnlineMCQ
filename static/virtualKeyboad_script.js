const keyboardContainer = document.getElementById('virtual-keyboard');
var textarea = null;
keyboardLayout = []
kbLayout = []
shifted = false

// const keyboardLayout = [
//     ['ক', 'খ', 'গ', 'ঘ', 'ঙ', 'চ', 'ছ', 'জ', 'ঝ', 'ঞ', 'ট', 'ঠ'],
//     ['ড', 'ঢ', 'ণ', 'ত', 'থ', 'দ', 'ধ', 'ন', 'প', 'ফ', 'ব', 'ভ'],
//     ['ম', 'য', 'র', 'ল', 'শ', 'ষ', 'স', 'হ', 'ড়', 'ঢ়', 'য়', 'ৎ'],
//     ['এ', 'ঐ', 'ও', 'ঔ', 'অ', 'আ', 'ই', 'ঈ', 'উ', 'ঊ', 'ঋ', 'ঌ'],
//     ['', '্', 'া', 'ি', 'ী', 'ু', 'ূ', 'ৃ', 'ে', 'ৈ', 'ো', 'ৌ'],
//     ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'],
//     ['Shift', 'Backspace', 'Space']
// ];

//unicode for all bengali vowels + consonants + numbers and Diacritics (অণুচিহ্ন) mapping
// const KeyboardLayoutUnicode = [
//     // অ   আ    ই     ঈ    উ     ঊ     ঋ    এ     ঐ    ও   
//     [2437, 2438, 2439, 2440, 2441, 2442, 2443, 2447, 2448, 2451],
//     // ঔ    ০    ১     ২     ৩     ৪     ৫    ৬     ৭     ৮
//     [2452, 2534, 2535, 2536, 2537, 2538, 2539, 2540, 2541, 2542],
//     // ৯    ক    খ     গ     ঘ    ঙ     চ     ছ     জ    ঝ
//     [2543, 2453, 2454, 2455, 2456, 2457, 2458, 2459, 2460, 2461],
//     // ঞ   ট     ঠ     ড     ঢ    ণ     ত     থ     দ     ধ
//     [2462, 2463, 2464, 2465, 2466, 2467, 2468, 2469, 2470, 2471],
//     // ন    প    ফ     ব     ভ    ম     য     র     ল    শ
//     [2472, 2474, 2475, 2476, 2477, 2478, 2479, 2480, 2482, 2486],
//     // ষ    স    হ     ড়     ঢ়     য়     ৎ      ঁ      ং     ঃ
//     [2487, 2488, 2489, 2524, 2525, 2527, 2510, 2433, 2434, 2435],
//     //'া'  'ি'   'ী'   'ু'    'ূ'   'ৃ'   'ে'   'ৈ'  'ো'  'ৌ'
//     [2494, 2495, 2496, 2497, 2498, 2499, 2503, 2504, 2507, 2508],
//     //'্'   ⇧   ⌫    
//     [2509, 8679, 9003, 32]
// ];

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
function createKeyboard(txtBoxID) {
    textarea = document.getElementById(txtBoxID);
    keyboardLayout.forEach(row => {
        row.forEach(key => {
            const keyElement = document.createElement('div');
            keyElement.classList.add('key');
            keyElement.textContent = key;

            if (key === String.fromCharCode('8679')) {
                keyElement.classList.add('special-key','shiftKey');
            }
            else if( key === String.fromCharCode('9003')){
                keyElement.classList.add('special-key','backspaceKey');
            }
            else if( key === String.fromCharCode('32')){
                keyElement.classList.add('special-key','spacebarKey');
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


