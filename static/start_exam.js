const totcontainer = document.querySelector('.tot-container');
const qheading1 = document.querySelector('.q-heading1');
const qheading2 = document.querySelector('.q-heading2');
const questionType = document.querySelector('.question-type');
const questionBox = document.querySelector('.question');
const choicesBox = document.querySelector('.choices');
const attachment = document.querySelector('.attachment');
const previousBtn = document.querySelector('.previousBtn');
const nextBtn = document.querySelector('.nextBtn');
const reviewBtn = document.querySelector('.reviewBtn');
const submitBtn = document.querySelector('.submitBtn');
const clearBtn = document.querySelector('.clearBtn');
const scoreCard = document.querySelector('.scoreCard');
// const alert = document.querySelector('.alert');
const timer = document.querySelector('.timer');
const qpallete = document.querySelector('.q-pallete');
const cmdPrimary = document.querySelector('.cmdPrimary');
const cmdSecondary = document.querySelector('.cmdSecondary');
// const sidebar = document.querySelector('.sidebar');

//for examinfo
const infoclass = document.querySelector('.infoclass');
const infosem = document.querySelector('.infosem');
const infoqtype = document.querySelector('.infoqtype');
const infochapter = document.querySelector('.infochapter');
const infoschedule = document.querySelector('.infoschedule');

const buttonGroup = document.getElementById("button-area");

const radioGroupName = 'myRadioGroup'; // All radio buttons in a group must have the same name

// Store questions, choices, correct answers
const questions = receivedData;

//store exam info
const examinfodata = examinfo[0];

// Making Variables
let currentQuestionIndex = 0;
let obtainedScore = 0;
let totalScore = 0;
// let questionsOver = false;

let countdownInterval = null;
let targetDate = null;

// const targetDate = new Date("Aug 22, 2025 12:59:59").getT ime();

// Arrow Function to Show Questions
const showQuestions = () => {

    const questionDetails = questions[currentQuestionIndex];

    //clears questiontype before every new questions
    questionType.innerHTML = ""
    //clears questiontype before every new questions
    questionBox.innerHTML = ""
    //clears choicebox before every new questions
    choicesBox.innerHTML = ""
    //clears attachment before every new question
    attachment.innerHTML = ""


    let qno = "Q." + String(currentQuestionIndex + 1) + ". " + questionDetails.questiontype
    questionType.textContent = qno

    // create question
    if (questionDetails.questiontype == 'Match the columns') {     //for match column question create table
        let array2d = splitStringInto2DArray(questionDetails.question);
        console.log(array2d);
        addTable(array2d);
    }
    else if (questionDetails.questiontype == 'Drag and Drop Type') {    //for Drag and Drop question type create list
        // Get the string from localStorage
        const localAnswer = localStorage.getItem("currentUserAnswer");

        // Parse the JSON string back into an object
        const userAnswerString = JSON.parse(localAnswer);

        const targetAnswer = userAnswerString.find(ans => ans.qno === currentQuestionIndex + 1);
        // if found in localstorage populate right list
        if (targetAnswer.qans !== "") {
            const side = "right";
            const allItems = targetAnswer.qans;
            addDragDropStack(side, allItems);
        }
        else {  //nothing is found in localstorage and hence populate left list
            const side = "left";
            const allItems = questionDetails.question;
            addDragDropStack(side, allItems);
        }

        //for disaster recovery
        setDisasterQuestionIndex(currentQuestionIndex);

        //retuns as no option is required
        return;
    }
    else {
        questionBox.textContent = questionDetails.question;
    }

    // creates option for the question
    const options = [
        { label: questionDetails.choices[0], value: questionDetails.choices[0] },
        { label: questionDetails.choices[1], value: questionDetails.choices[1] },
        { label: questionDetails.choices[2], value: questionDetails.choices[2] },
        { label: questionDetails.choices[3], value: questionDetails.choices[3] }
    ]

    const choicename = ["A.", "B.", "C.", "D.", "E.", "F."];

    const radioGroupName = 'myRadioGroup'; // All radio buttons in a group must have the same name

    let x = 0;

    options.forEach(item => {

        // Displays choice name e.g. A, B, C, B etc
        const choicediv = document.createElement('label');
        choicediv.textContent = choicename[x]
        choicesBox.appendChild(choicediv)

        const newdiv = document.createElement('div');
        newdiv.classList.add('form-check')
        newdiv.style.display = 'inline-block'
        newdiv.style.paddingLeft = "40px"
        choicesBox.appendChild(newdiv)

        // Create input element for radio button
        const radioInput = document.createElement('input');
        radioInput.type = 'radio';
        radioInput.name = radioGroupName;
        radioInput.value = item.value;
        radioInput.id = x; // Assign a unique ID for the label to reference
        radioInput.classList.add('form-check-input')

        // Create label element for the radio button
        const radioLabel = document.createElement('label');
        radioLabel.htmlFor = x; // Link label to input using its ID
        radioLabel.textContent = item.label;
        radioLabel.classList.add('form-check-label')

        // Append radio button and label to the mainContent
        newdiv.appendChild(radioInput);
        newdiv.appendChild(radioLabel);

        // newdiv.appendChild(document.createElement('br')); // Optional: for line breaks

        // Displays break before each choice
        const breakdiv = document.createElement('br');
        choicesBox.appendChild(breakdiv)
        x++;

    });

    //insert image if question contains an image
    if (questions[currentQuestionIndex].hasimage == "Yes") {

        // Create a new image element
        const img = document.createElement('img');

        // Set the image source
        img.src = '/static/upload_files/' + questions[currentQuestionIndex].imagelocation;
        console.log(img.src)
        // Optional: Set alt text for accessibility
        img.alt = 'Description of the image';

        // Optional: Set width and height
        img.width = 200;
        img.height = 150;

        // Append the image to the div
        attachment.appendChild(img);
    }

    //set radio answer if stored previously in localstorage
    getAnswerLocalStorage(currentQuestionIndex)

    //for disaster recovery
    setDisasterQuestionIndex(currentQuestionIndex);

}

//Function to create Table
function addTable(array2d) {
    // var myTableDiv = document.getElementById("myDynamicTable");

    const table = document.createElement('table');
    table.classList.add('table', 'table-bordered', 'table-sm');

    const thead = document.createElement('thead');
    thead.classList.add('thead-light')
    const tbody = document.createElement('tbody');
    table.appendChild(thead);
    table.appendChild(tbody);

    const headerRow = document.createElement('tr');
    const headers = ['Column A', 'Column B'];
    headers.forEach(headerText => {
        const th = document.createElement('th');
        th.setAttribute('scope', "col");
        th.textContent = headerText;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);

    for (var i = 0; i < 4; i++) {
        const tr = document.createElement('tr');
        tr.setAttribute('scope', 'row');
        tbody.appendChild(tr);

        for (var j = 0; j < 2; j++) {
            const td = document.createElement('td');
            td.appendChild(document.createTextNode(array2d[i][j]));
            tr.appendChild(td);
        }
    }
    questionBox.appendChild(table);

}

//Function to create Drag and Drop list
function addDragDropStack(side, allitems) {
    // console.log(side, allitems)
    itemlist = allitems.split('/');

    const DragDropContainer = document.createElement('div');
    DragDropContainer.classList.add('DragDropContainer');
    questionBox.appendChild(DragDropContainer);

    const listleft = document.createElement('div');
    listleft.id = "left";
    DragDropContainer.appendChild(listleft);

    const listright = document.createElement('div');
    listright.id = "right";
    DragDropContainer.appendChild(listright);

    itemlist.forEach((element, index) => {

        const newDiv = document.createElement('div');
        newDiv.classList.add('list');
        newDiv.setAttribute('draggable', "true");

        const newimg = document.createElement('img');
        newimg.src = "/static/images/dragicon.png";
        newimg.alt = "";
        newDiv.appendChild(newimg);

        // Create the text element 
        const textElement = document.createElement('span');
        // Create the text node
        const textNode = document.createTextNode(String(element));
        // Append the text node to the text element
        textElement.appendChild(textNode);
        newDiv.appendChild(textElement);

        if (side == 'left') {
            listleft.appendChild(newDiv);
        }

        if (side == 'right') {
            listright.appendChild(newDiv);
        }
    });


    // add the draggable event to the list items
    let lists = document.getElementsByClassName('list');
    let leftBox = document.getElementById('left');
    let rightBox = document.getElementById('right');

    for (list of lists) {
        list.addEventListener("dragstart", (e) => {
            let selected = e.target;

            //for left to right drag
            rightBox.addEventListener('dragover', (e) => {
                e.preventDefault();
            })
            rightBox.addEventListener('drop', () => {
                rightBox.appendChild(selected);
                selected = null;  /* so that new one can be dragged*/
            })

            //for right to left drag (copied from above)
            leftBox.addEventListener('dragover', (e) => {
                e.preventDefault();
            })
            leftBox.addEventListener('drop', () => {
                leftBox.appendChild(selected);
                selected = null;
            })
        })
    }

}

//Function Drag and Drop answer status
function DragDropAnswerStatus() {
    // count no of items in the left list
    const leftDDlist = questions[currentQuestionIndex].question.split('/');
    const leftDDlistLength = leftDDlist.length;

    // count no of items in the riht list
    const parentDiv = document.getElementById('right');
    const directChildren = Array.from(parentDiv.children); // Convert HTMLCollection to an array
    const divChildren = directChildren.filter(child => child.tagName === 'DIV'); // Filter for 'div' elements
    const rightDDlistLength = divChildren.length;

    let allSpanTexts = "";

    if (leftDDlistLength === rightDDlistLength) {
        const myDiv = document.getElementById('right');
        const spans = myDiv.getElementsByTagName('span');
        // const allSpanTexts = [];
        // for (let i = 0; i < spans.length; i++) {
        //     allSpanTexts.push(spans[i].textContent);
        // }
        for (let i = 0; i < spans.length; i++) {
            i == 0 ? allSpanTexts = spans[i].textContent : allSpanTexts = allSpanTexts + "/" + spans[i].textContent
        }
    }
    else {
        allSpanTexts = "";
    }

    return allSpanTexts;
}

// Function to check answers
const checkAnswer = () => {
    // Get the string from localStorage
    const storedLocalAnswer = localStorage.getItem("currentUserAnswer");
    // Parse the JSON string back into an object
    const answerString = JSON.parse(storedLocalAnswer);

    for (let i = 0; i < answerString.length; i++) {
        if (answerString[i].cans === answerString[i].qans) {
            obtainedScore++;
        }
    }
}


// Function to show score
//const showScore = () => {
// qheading1.style.display = "none";
// qheading2.style.display = "none";
// questionType.style.display = "none";
// questionBox.style.display = "none";
// choicesBox.style.display = "none";
// attachment.style.display = "none";
// cmdPrimary.style.display = "none";
// cmdSecondary.style.display = "none";
// qpallete.style.display = "none";
// timer.style.display = "none";

// const imageContainer = document.querySelector('.scoreCard');
// const newImage = document.createElement('img');
// newImage.src = '/staic/images/Congratulations.png'; 
// newImage.alt = 'A placeholder image';
// newImage.style.maxWidth = '100%'; 
// imageContainer.appendChild(newImage);

// scoreCard.classList.add('scorecardstyle');
// scoreCard.textContent = `You Scored ${score} out of ${questions.length}!`;
//}

// Function to Show Alert
// const displayAlert = (msg) => {
//     alert.style.display = "block";
//     alert.textContent = msg;
//     setTimeout(()=>{
//         alert.style.display = "none";
//     }, 2000);
// }


// Function to Start Timer
const startTimer = () => {

    countdownInterval = setInterval(function () {
        const now = new Date().getTime();
        const distance = targetDate - now;

        // const days = String(Math.floor(distance / (1000 * 60 * 60 * 24))).padStart(2, '0');
        const hours = String(Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))).padStart(2, '0');
        const minutes = String(Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60))).padStart(2, '0');
        const seconds = String(Math.floor((distance % (1000 * 60)) / 1000)).padStart(2, '0');

        timer.innerHTML = `${hours} : ${minutes} : ${seconds}`;

        //store timeleft periodically to retrieve in disaster situation
        localStorage.setItem('timeLeft', timer.innerHTML);

        if (distance < 0) {
            clearInterval(countdownInterval);

            //check the answers
            checkAnswer();

            //set values for flask route parameter
            const param_obtainedScore = obtainedScore;
            const param_totalScore = questions.length;

            // Get the string from localStorage
            const localanswer = localStorage.getItem("currentUserAnswer");
            const param_answerMatrix = JSON.parse(localanswer);

            //clears all local storage items
            localStorage.clear();

            // Using fetch API to send answer matrix to flask
            fetch('/score/api/process_answerMatrix_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(param_answerMatrix)
            })
                .then(response => {
                    // Handle the response from the Flask endpoint
                    // This could be a success message, or a URL for redirection
                    return response.json(); // If Flask sends back JSON
                })
                .then(data => {
                    // After successfully sending data, now redirect

                    // Construct the URL with parameters
                    const targetUrl = `/score/${param_obtainedScore}/${param_totalScore}`;
                    window.location.href = targetUrl;

                })
                .catch(error => console.error('Error:', error));


        }
    }, 1000);
}

// Function to Stop Timer
const stopTimer = () => {
}

// Function to shuffle question
// const shuffleQuestions = () =>{
//     for(let i=questions.length-1; i>0; i--){
//         const j = Math.floor(Math.random() * (i+1));
//         [questions[i], questions[j]] = [questions[j], questions[i]];
//     }
//     currentQuestionIndex = 0;
//     showQuestions();
// }


// Function to Start questions
const startquestions = () => {
    timer.style.display = "flex";
    // shuffleQuestions();
    showQuestions()
}

// Adding Event Listener to Submit Button
submitBtn.addEventListener('click', () => {
    //shows confirmation window
    let userConfirmed = confirm("Are you sure to submit the exam ?");

    if (userConfirmed) {
        // User clicked "OK" and starts the submit process
        clearInterval(countdownInterval);

        //check the answers
        checkAnswer();

        //set values for flask route parameter
        const param_obtainedScore = obtainedScore;
        const param_totalScore = questions.length;

        // Get the string from localStorage
        const localanswer = localStorage.getItem("currentUserAnswer");
        const param_answerMatrix = JSON.parse(localanswer);
        // console.log(localanswer)
        // console.log(param_answerMatrix)

        //clears all local storage items
        localStorage.clear();

        // Using fetch API to send answer matrix to flask
        fetch('/score/api/process_answerMatrix_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(param_answerMatrix)
        })
            .then(response => {
                // Handle the response from the Flask endpoint
                // This could be a success message, or a URL for redirection
                return response.json(); // If Flask sends back JSON
            })
            .then(data => {
                // After successfully sending data, now redirect

                // Construct the URL with parameters
                const targetUrl = `/score/${param_obtainedScore}/${param_totalScore}`;
                window.location.href = targetUrl;

            })


    } else {
        // User clicked "Cancel" and do nothing
    }

});

nextBtn.addEventListener('click', () => {
    const selectedButton = document.getElementById("button" + String(currentQuestionIndex + 1));
    review = "";

    switch (questions[currentQuestionIndex].questiontype) {

        // for Drag and Drop Type
        case 'Drag and Drop Type':
            const status = DragDropAnswerStatus();
            // console.log(status)
            if (status.length > 0) {
                //set the legends
                setLegend(selectedButton, 'butn-answered');
                //save answer in the local storage
                setAnswerLocalStorage(status, review);

            }
            else {
                //set the legends
                setLegend(selectedButton, 'butn-not-answered');
                //save answer in the local storage in case of clear response
                setAnswerLocalStorage(status, review);
            }
            break;

        default:
            if (isAnyOptionSelected()) {

                //set the legends
                setLegend(selectedButton, 'butn-answered');

                //save answer in the local storage
                var selectedRadio = document.querySelector('input[name="myRadioGroup"]:checked');
                updatedAnswer = selectedRadio.value;
                setAnswerLocalStorage(updatedAnswer, review);
            }
            else {
                //set the legends
                setLegend(selectedButton, 'butn-not-answered');

                //save answer in the local storage in case of clear response
                updatedAnswer = "";
                setAnswerLocalStorage(updatedAnswer, review);
            }
    }


    //show next question - if last repeat from 1st question
    currentQuestionIndex++;
    if (currentQuestionIndex < questions.length) {
        showQuestions();
    }
    else {
        currentQuestionIndex = 0;
        showQuestions();
    }
});

// function to check wheather any option is selected or not
function isAnyOptionSelected() {
    var selectedRadio = document.querySelector('input[name="myRadioGroup"]:checked');
    if (selectedRadio) {
        return true;
    }
    else {
        return false;
    }
}

//function to set the legend in question pallette
function setLegend(selectedButton, legend) {
    selectedButton.className = '';
    selectedButton.classList.add(legend)
}

reviewBtn.addEventListener('click', () => {

    //set the legend
    const selectedButton = document.getElementById("button" + String(currentQuestionIndex + 1));
    setLegend(selectedButton, 'butn-checkedforreview');

    //save answer in the local storage
    review = "R";
    if (isAnyOptionSelected()) {
        var selectedRadio = document.querySelector('input[name="myRadioGroup"]:checked');
        updatedAnswer = selectedRadio.value;
        setAnswerLocalStorage(updatedAnswer, review);
    }
    else {
        //save answer in the local storage in case of clear response
        updatedAnswer = "";
        setAnswerLocalStorage(updatedAnswer, review);
    }

    checkAnswer();

    //show next question - if last repeat from 1st question
    currentQuestionIndex++;
    if (currentQuestionIndex < questions.length) {
        showQuestions();
    }
    else {
        currentQuestionIndex = 0;
        showQuestions();
    }
})

previousBtn.addEventListener('click', () => {

    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        showQuestions();
    }
    else {
        currentQuestionIndex = questions.length - 1;
        showQuestions();
    }
})

clearBtn.addEventListener('click', () => {
    clearOptionSelection()
})
function splitStringInto2DArray(inputString) {
    // Split the string by '/'
    const firstSplit = inputString.split('/');

    // Map over the first split array and split each element by ','
    const final2DArray = firstSplit.map(subString => subString.split(','));

    return final2DArray;
}

//creates buttons for each question in question pallete
function createQuestionPallete(length) {
    for (let i = 0; i < length; i++) {

        const button = document.createElement("button");
        button.classList.add('butn-not-visited')
        button.id = "button" + String(i + 1);
        button.textContent = i + 1;
        button.value = i + 1;

        // Add event listener to each buttons of question palette
        button.addEventListener("click", () => {
            // alert(`You clicked: ${label}`);
            currentQuestionIndex = button.value - 1;
            showQuestions();
        });

        // newDiv.appendChild(button);
        buttonGroup.appendChild(button)
    }

}

// on page load prepares question pallete
document.addEventListener("DOMContentLoaded", function () {

    //add exam information
    infoclass.innerHTML = "Class : " + examinfodata.Class;
    infosem.innerHTML = "Sem : " + examinfodata.Sem;
    infoqtype.innerHTML = "QuestionType : " + examinfodata.QuestionType;
    infochapter.innerHTML = "Chapter : " + examinfodata.Chapter;
    infoschedule.innerHTML = "Schedule : " + examinfodata.Schedule;


    //add buttons to question palette
    createQuestionPallete(questions.length);

    //create object for storing answer to localstorage if only not already present
    const storedLocalAnswer = localStorage.getItem("currentUserAnswer");
    if (!storedLocalAnswer) {
        createLocalStorage(questions);
    }
    else {
        // Parse the JSON string back into an object
        const localAnswer = JSON.parse(storedLocalAnswer);

        //set the legends for previous saved answers
        for (let i = 0; i < questions.length; i++) {
            const selectedButton = document.getElementById("button" + String(i + 1));

            let answer = localAnswer[i].qans;
            let review = localAnswer[i].qreview;
            let notvisited = localAnswer[i].qnotVisited;

            if (notvisited === "NV") {
                setLegend(selectedButton, 'butn-not-visited');
            }
            else if (review === "R") {
                setLegend(selectedButton, 'butn-checkedforreview');
            }
            else if (answer === "") {
                setLegend(selectedButton, 'butn-not-answered');
            }
            else {
                setLegend(selectedButton, 'butn-answered');
            }

        }
    }

    setTargetDate();
    startTimer();

    //retrieve disaster question from localstorage
    const disaterquestion = localStorage.getItem("disasterCurrentQuestionIndex");
    if (disaterquestion) {
        currentQuestionIndex = Number(disaterquestion);
    }

    startquestions();

    // sidebar.style.display = "none";
});

//create initial blank answer for storage
function createLocalStorage(questions) {
    let localAnswer = [];

    for (let i = 0; i < questions.length; i++) {
        let answerObject = {
            qno: i + 1,
            qreview: "",
            qnotVisited: "NV",
            qid: questions[i].id,
            qans: "",
            cans: questions[i].answer
        };
        localAnswer.push(answerObject);
    }

    //Convert the object to a JSON string
    const userAnswerString = JSON.stringify(localAnswer);

    //Store the string in localStorage
    localStorage.setItem("currentUserAnswer", userAnswerString);
}

//save answer in local storage on click of'save and next' or 'mark for review' button
function setAnswerLocalStorage(updatedAnswer, review) {
    // Get the string from localStorage
    const storedLocalAnswer = localStorage.getItem("currentUserAnswer");
    // Parse the JSON string back into an object
    const answerString = JSON.parse(storedLocalAnswer);

    // Modify the found object
    const targetAnswer = answerString.find(ans => ans.qno === currentQuestionIndex + 1);
    if (targetAnswer) {
        targetAnswer.qans = updatedAnswer;
        targetAnswer.qreview = review;
        //set noy visited to false
        targetAnswer.qnotVisited = "";
    }

    //Convert the object to a JSON string
    const updatedanswerString = JSON.stringify(answerString);
    //Store the string in localStorage
    localStorage.setItem("currentUserAnswer", updatedanswerString);
}

//fetch answer from localstorage if any and select radio button accordingly
function getAnswerLocalStorage(currentQuestionIndex) {
    // Get the string from localStorage
    const localAnswer = localStorage.getItem("currentUserAnswer");

    // Parse the JSON string back into an object
    const userAnswerString = JSON.parse(localAnswer);

    const targetAnswer = userAnswerString.find(ans => ans.qno === currentQuestionIndex + 1);

    if (targetAnswer !== '') {
        // targetUser.username = 'updatedUser2'; // Modify the found object
        setSelectedOption(targetAnswer.qans)

    }
}

//this function works with getAnswerLocalStorage()
function setSelectedOption(selectedValue) {

    const radioButtons = document.getElementsByName(radioGroupName); // Get all radio buttons with the name radioGroupName variable

    for (let i = 0; i < radioButtons.length; i++) {
        if (radioButtons[i].value === selectedValue) {
            radioButtons[i].checked = true; // Set the 'checked' property to true for the matching radio button
            break; // Exit the loop once the option is found and checked
        }
    }
}

//function to clear any answer selected
function clearOptionSelection(radioGroupName) {
    const radioButtons = document.querySelectorAll('input[name="myRadioGroup"]');
    radioButtons.forEach(button => {
        button.checked = false;
    });
}

function setTargetDate() {
    // retrives scheduled datetime
    let isoDateString = examinfodata['Schedule']
    let dateObject = new Date(isoDateString);
    let scheduledDatetime = dateObject.toLocaleString();
    let sch_datetime = new Date(scheduledDatetime)
    let examtimedomain = Number(examinfodata['ExamTimeDomain']); // Number of minutes to add
    sch_datetime.setMinutes(sch_datetime.getMinutes() + examtimedomain);


    // constructs current datetime
    let myDate = new Date();
    let currentDatetime = myDate.toLocaleString();
    let cur_datetime = new Date(currentDatetime);

    //disaster time recovery
    disasterTime = localStorage.getItem('timeLeft');

    if (disasterTime) {
        let parts = disasterTime.split(':');
        cur_datetime.setHours(cur_datetime.getHours() + Number(parts[0]), cur_datetime.getMinutes() + Number(parts[1]), cur_datetime.getSeconds() + Number(parts[2]));
    }
    else {
        let examduration = Number(examinfodata['ExamDuration']);
        cur_datetime.setMinutes(cur_datetime.getMinutes() + examduration);
    }

    if (cur_datetime < sch_datetime) {
        targetDate = cur_datetime;
    }
    else {
        targetDate = sch_datetime;
    }
}

//Store the current question in localStorage (for Disaster Management)
function setDisasterQuestionIndex(currentQuestionIndex) {
    localStorage.setItem("disasterCurrentQuestionIndex", currentQuestionIndex);
}