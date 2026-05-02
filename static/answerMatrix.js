const tableData = receivedData;
const qbank = questionBank;
const examinfo = exinfo;
const isoldresult = ior;

let score = 0;
let total = 0;

document.addEventListener('DOMContentLoaded', function () {

    //calculate score and total
    for (let i = 0; i < tableData.length; i++) {
        total++;
        if (tableData[i].qans === tableData[i].cans) {
            score++;
        }
    }

    // fill examinfo information
    displayExamInfo();


    // Call the function to create the table
    createDynamicTable(tableData, 'table-container');
    initializeTooltips();

    // enable or disable Exit Exam Button
    if (isoldresult[0].old === "Yes") {
        const exitexambtn = document.getElementById('exitExamBtn');
        exitexambtn.style.display = "none"
    }
});

function createDynamicTable(data, containerId) {
    const container = document.getElementById(containerId);
    if (!container) {
        console.error('Container element not found!');
        return;
    }


    // Clear existing content if any
    container.innerHTML = '';

    const table = document.createElement('table');
    table.classList.add('table', 'table-bordered', 'table-responsive', 'table-sm', 'tableCss');

    // Create table header
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    const headers = ['QNo.', 'QID', 'Your Answer', 'Correct Answer'];

    headers.forEach(headerText => {
        const th = document.createElement('th');
        th.textContent = headerText;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Create table body
    const tbody = document.createElement('tbody');

    data.forEach(rowData => {
        const row = document.createElement('tr');

        const cell1 = document.createElement('td');
        cell1.textContent = rowData['qno'];
        row.appendChild(cell1);

        //get answer Matix Details from question id
        qid = rowData['qid'];
        q = getQueationDetails(qid);

        //add bootstrap tooltip for question details
        const cell2 = document.createElement('td');
        cell2.innerHTML = `<span data-bs-toggle="tooltip" data-bs-placement="bottom" title='${q}'>${qid}</span>`;
        initializeTooltips(); // Re-initialize tooltips after adding new elements
        row.appendChild(cell2);

        const cell3 = document.createElement('td');
        const val1 = rowData['qans']
        const val2 = rowData['cans']
        if (val1 === "") {
            const newDiv = document.createElement('div')
            newDiv.textContent = "Not Answered";
            newDiv.classList.add('notAnswered')
            cell3.appendChild(newDiv)
        }
        else if (val1 === val2) {
            const newDiv = document.createElement('div')
            newDiv.textContent = val1;
            newDiv.classList.add('correctAnswer')
            cell3.appendChild(newDiv)
        }
        else {
            const newDiv = document.createElement('div')
            newDiv.textContent = val1;
            newDiv.classList.add('wrongAnswer')
            cell3.appendChild(newDiv)
        }
        row.appendChild(cell3);

        const cell4 = document.createElement('td');
        cell4.textContent = rowData['cans'];
        row.appendChild(cell4);

        tbody.appendChild(row);
    });
    table.appendChild(tbody);

    container.appendChild(table);
}

function getQueationDetails(qid) {
    // Find a question by their ID
    const question_details = qbank.find(q => q.id === Number(qid));
    question = question_details.question;
    return question;
}

function initializeTooltips() {
    // For Bootstrap 5+
    // var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    // var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    //     return new bootstrap.Tooltip(tooltipTriggerEl)
    // })

    // For Bootstrap 5
    $('[data-bs-toggle="tooltip"]').tooltip();
    // For Bootstrap 3/4 
    $('[data-toggle="tooltip"]').tooltip();
}

function displayExamInfo() {
    const cl = document.getElementById('cl');
    const sem = document.getElementById('sem');
    const schedule = document.getElementById('schedule');
    const qtype = document.getElementById('qtype');
    const chapter = document.getElementById('chapter');
    const qtime = document.getElementById('qtime');
    const duration = document.getElementById('duration');
    const scored = document.getElementById('score');
    const totalM = document.getElementById('total');


    cl.textContent = "Class : " + examinfo[0]['Class'];
    sem.textContent = "Semester : " + examinfo[0]['Sem'];

    // Create a DateTimeFormat instance for a specific locale (e.g., 'en-IN')
    const formatter = new Intl.DateTimeFormat('en-IN', options);
    // Format the date
    let sdate = new Date(examinfo[0]['Schedule'])
    const formattedDate = formatter.format(sdate);

    schedule.textContent = "Schedule : " + formattedDate;

    qtype.textContent = "Question Type : " + examinfo[0]['QuestionType'];
    chapter.textContent = "Chapter : " + examinfo[0]['Chapter'];

    qtime.textContent = "Exam Duration : " + examinfo[0]['ExamDuration'] + " Minutes";
    duration.textContent = "Exam Time Domain : " + examinfo[0]['ExamTimeDomain'] + " Minutes";

    scored.textContent = "You Scored : " + score;
    totalM.textContent = "Total Marks : " + total;
}

// Define options for the desired custom format
const options = {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
};

// createPdfBtn.addEventListener('click', function () {
//     // Get the entire HTML content of the current page as string
//     const currentPageHTML = document.documentElement.innerHTML;

//     // AJAX request to send html content to flask
//     fetch('/receive-html', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ html_content: currentPageHTML })
//     })
//     .then(response => response.json())
//     .then(data => console.log(data))
//     .catch(error => console.error('Error:', error));
// });

