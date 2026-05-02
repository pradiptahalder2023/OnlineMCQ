// const qclass = document.getElementById('qclass');
// const qsem = document.getElementById('qsem');
// const qchapter = document.getElementById('qchapter');
// const qtype = document.getElementById('qtype');

// // Select the primary checkbox and the group of checkboxes
// // let selectAllQtype = '';
// // let otherCheckQtype = '';

// //on load of the form
// document.addEventListener('DOMContentLoaded', function () {

//     //populates class selectbox dynamically
//     fetch('/api/get_studyClass') // AJAX request to Flask route
//         .then(response => response.json())
//         .then(data => {

//             qclass.innerHTML = ''; // Clear existing options

//             // Create the blank/placeholder option
//             const blankOption = document.createElement('option');
//             blankOption.value = ''; // Assign an empty value
//             blankOption.textContent = 'Please select Class...'; // Display text
//             blankOption.selected = true; // Make it the default selected option
//             blankOption.disabled = true; // Optionally disable it after initial selection
//             qclass.appendChild(blankOption);

//             data.forEach(function (class_List) {
//                 var option = document.createElement('option');
//                 option.value = class_List.cl_desc;
//                 option.textContent = class_List.cl_desc;
//                 qclass.appendChild(option);

//             });

//         });

//     //populates Questiontype selectbox dynamically
//     fetch('/api/get_QuestionType') // AJAX request to Flask route
//         .then(response => response.json())
//         .then(data => {
//             qtype.innerHTML = ''; // Clear existing options

//             // Create the <ul> element
//             const qtypelist = document.createElement('ul');

//             // Create the blank/placeholder option
//             const blankOption = document.createElement('option');
//             blankOption.value = ''; // Assign an empty value
//             blankOption.textContent = 'Please select Type of Question...'; // Display text
//             blankOption.selected = true; // Make it the default selected option
//             blankOption.disabled = true; // Optionally disable it after initial selection
//             qtypelist.appendChild(blankOption);

//             // Create the 'ALL' question type option

//             // const allOption = document.createElement('option');
//             // allOption.value = '0'; // Assign an empty value
//             // allOption.textContent = 'ALL'; // Display text
//             // qtype.appendChild(allOption);

//             let li = document.createElement('li');
//             let checkbox = document.createElement('input');
//             checkbox.type = 'checkbox';
//             checkbox.name = 'qtype'; // Must match the field name in WTForms
//             checkbox.value = '0';
//             checkbox.id = 'chkQtypeAll';

//             let label = document.createElement('label');
//             label.htmlFor = checkbox.id;
//             label.appendChild(document.createTextNode('ALL'));

//             li.appendChild(checkbox);
//             li.appendChild(label);
//             qtypelist.appendChild(li);


//             data.forEach(function (qtype_List) {

//                 // var option = document.createElement('option');
//                 // option.value = qtype_List.id;
//                 // option.textContent = qtype_List.qtype_desc;
//                 // qtype.appendChild(option);

//                 // Create a container for the checkbox and label
//                 let li = document.createElement('li');
//                 let checkbox = document.createElement('input');
//                 checkbox.type = 'checkbox';
//                 checkbox.name = 'qtype'; // Must match the field name in WTForms
//                 checkbox.value = qtype_List.id;
//                 checkbox.id = qtype_List.id;
//                 checkbox.className = 'chkQtypeOther'

//                 let label = document.createElement('label');
//                 label.htmlFor = checkbox.id;
//                 label.appendChild(document.createTextNode(qtype_List.qtype_desc));

//                 li.appendChild(checkbox);
//                 li.appendChild(label);
//                 qtypelist.appendChild(li);
//             });
//             qtype.appendChild(qtypelist);

//             // selectAllQtype = document.getElementById('chkQtypeAll');

//             // otherCheckQtype = document.querySelectorAll('.chkQtypeOther');
//         });
// });

// //on change class, populate sem
// qclass.addEventListener('change', function () {
//     var selected_class = this.value;
//     fetch('/api/get_semester/' + selected_class) // AJAX request to Flask route
//         .then(response => response.json())
//         .then(data => {
//             qsem.innerHTML = ''; // Clear existing options

//             // Create the blank/placeholder option
//             const blankOption = document.createElement('option');
//             blankOption.value = ''; // Assign an empty value
//             blankOption.textContent = 'Please select Semester...'; // Display text
//             blankOption.selected = true; // Make it the default selected option
//             blankOption.disabled = true; // Optionally disable it after initial selection
//             qsem.appendChild(blankOption);

//             data.forEach(function (semester) {
//                 var option = document.createElement('option');
//                 option.value = semester.sm_desc;
//                 option.textContent = semester.sm_desc;
//                 qsem.appendChild(option);
//             });
//         });
// });

// //on change sem, populate chapter
// qsem.addEventListener('change', function () {
//     let selected_class = qclass.value;
//     let selected_sem = this.value;
//     fetch('/api/get_chapter/' + selected_class + '/' + selected_sem) // AJAX request to Flask route
//         .then(response => response.json())
//         .then(data => {
//             qchapter.innerHTML = ''; // Clear existing options

//             // Create the <ul> element
//             const chapterlist = document.createElement('ul');

//             // Create the blank/placeholder option
//             const blankOption = document.createElement('option');
//             blankOption.value = ''; // Assign an empty value
//             blankOption.textContent = 'Please select Chapter...'; // Display text
//             blankOption.selected = true; // Make it the default selected option
//             blankOption.disabled = true; // Optionally disable it after initial selection
//             chapterlist.appendChild(blankOption);

//             // check if the returned json is empty or not
//             const isEmpty = Object.keys(data).length === 0;

//             if (!isEmpty) {

//                 // Create the 'ALL' question type option
//                 // const allOption = document.createElement('option');
//                 // allOption.value = '0'; // Assign an empty value
//                 // allOption.textContent = 'ALL'; // Display text
//                 // qchapter.appendChild(allOption);
//                 let li = document.createElement('li');
//                 let checkbox = document.createElement('input');
//                 checkbox.type = 'checkbox';
//                 // checkbox.className = 'form-check-input';
//                 checkbox.name = 'qchapter'; // Must match the field name in WTForms
//                 checkbox.value = '0';
//                 // checkbox.id = '0';
//                 checkbox.id = 'chkChapterAll';

//                 let label = document.createElement('label');
//                 // label.className = 'form-check-label'
//                 label.htmlFor = checkbox.id;
//                 label.appendChild(document.createTextNode('ALL'));

//                 li.appendChild(checkbox);
//                 li.appendChild(label);
//                 chapterlist.appendChild(li);


//                 data.forEach(function (chapter) {
//                     // var option = document.createElement('option');
//                     // option.value = chapter.ch_no;
//                     // option.textContent = chapter.ch_desc;
//                     // qchapter.appendChild(option);

//                     // Create a container for the checkbox and label
//                     let li = document.createElement('li');
//                     let checkbox = document.createElement('input');
//                     checkbox.type = 'checkbox';
//                     checkbox.name = 'qchapter'; // Must match the field name in WTForms
//                     checkbox.value = chapter.ch_no;
//                     checkbox.id = chapter.ch_no;
//                     checkbox.className = 'chkChapterOther';

//                     let label = document.createElement('label');
//                     label.htmlFor = checkbox.id;
//                     label.appendChild(document.createTextNode(chapter.ch_desc));

//                     li.appendChild(checkbox);
//                     li.appendChild(label);
//                     chapterlist.appendChild(li);
//                 });
//             }
//             qchapter.appendChild(chapterlist)
//         });
// });


// // //on change chapter, displays question
// // qsem.addEventListener('change', function () {
// //     var selected_class = qclass.value;
// //     var selected_sem = this.value;
// //     fetch('/api/get_chapter/' + selected_class + '/' + selected_sem) // AJAX request to Flask route
// //         .then(response => response.json())
// //         .then(data => {
// //             qchapter.innerHTML = ''; // Clear existing options

// //             // Create the blank/placeholder option
// //             const blankOption = document.createElement('option');
// //             blankOption.value = ''; // Assign an empty value
// //             blankOption.textContent = 'Please select Chapter...'; // Display text
// //             blankOption.selected = true; // Make it the default selected option
// //             blankOption.disabled = true; // Optionally disable it after initial selection
// //             qchapter.appendChild(blankOption);

// //             data.forEach(function (semester) {
// //                 var option = document.createElement('option');
// //                 option.value = semester.ch_desc;
// //                 option.textContent = semester.ch_desc;
// //                 qchapter.appendChild(option);
// //             });
// //         });
// // });




// // on selectall qtype disables other checkboxes
// $(document).on('change', '#chkQtypeAll', function () {
//     // Get the current checked state (true or false)
//     var isChecked = $(this).prop('checked');

//     // Disable other checkboxes if 'Select All' is checked
//     $('.chkQtypeOther').prop('disabled', isChecked);

//     // Optional: If you also want to check/uncheck them automatically
//     $('.chkQtypeOther').prop('checked', isChecked);
// });

// // on selectall Chapter disables other checkboxes
// $(document).on('change', '#chkChapterAll', function () {
//     // Get the current checked state (true or false)
//     var isChecked = $(this).prop('checked');

//     // Disable other checkboxes if 'Select All' is checked
//     $('.chkChapterOther').prop('disabled', isChecked);

//     // Optional: If you also want to check/uncheck them automatically
//     $('.chkChapterOther').prop('checked', isChecked);
// });

$(document).ready(function () {
    // 1. Form লোডে qclass আর qtype লোড
    loadClasses();
    loadQTypes();

    // 2. qclass চেঞ্জ হলে qsem লোড
    $('#qclass').change(function () {
        let class_id = $(this).val();
        loadSemesters(class_id);
        loadChapters(0, 0);
    });

    // 3. qsem চেঞ্জ হলে qchapter লোড
    $('#qsem').change(function () {
        let class_id = $('#qclass').val();
        let sem_id = $(this).val();
        loadChapters(class_id, sem_id);
    });

    // 4. ALL লজিক - qtype: ALL চেক করলে বাকিগুলো ডিজেবল
    $(document).on('change', '#qtype-0', function () {
        let checked = $(this).prop('checked');
        $('input[name="qtype"]').not('#qtype-0').prop('checked', false).prop('disabled', checked);
    });

    $(document).on('change', 'input[name="qtype"]:not(#qtype-0)', function () {
        if ($('input[name="qtype"]:not(#qtype-0):checked').length > 0) {
            $('#qtype-0').prop('checked', false);
        }
    });

    // 5. ALL লজিক - qchapter: ALL চেক করলে বাকিগুলো ডিজেবল
    $(document).on('change', '#qchapter-0', function () {
        let checked = $(this).prop('checked');
        $('input[name="qchapter"]').not('#qchapter-0').prop('checked', false).prop('disabled', checked);
    });

    $(document).on('change', 'input[name="qchapter"]:not(#qchapter-0)', function () {
        if ($('input[name="qchapter"]:not(#qchapter-0):checked').length > 0) {
            $('#qchapter-0').prop('checked', false);
        }
    });
});

function loadClasses() {
    $.getJSON('/api/get_studyClass', function (data) {
        let select = $('#qclass');
        select.empty().append('<option value="0">-- Select Class --</option>');
        $.each(data, function (i, item) {
            select.append(`<option value="${item.cl_desc}">${item.cl_desc}</option>`);
        });
    });
}

function loadSemesters(class_id) {

    if (!class_id || class_id == 0) return;
    $.getJSON('/api/get_semester/' + class_id, function (data) {
        let select = $('#qsem');
        select.empty().append('<option value="0">-- Select Semester --</option>');
        console.log(data.length)
        $.each(data, function (i, item) {
            select.append(`<option value="${item.sm_desc}">${item.sm_desc}</option>`);
        });
    });
}

function loadQTypes() {
    $.getJSON('/api/get_QuestionType', function (data) {
        let area = $('#qtype');
        let html = '<ul>';
        html += `
                <li>
                    <input type="checkbox" name="qtype" value="0" id="qtype-0">
                    <label for="qtype-0"><b>ALL Types</b></label>
                </li>
            `;
        $.each(data, function (i, item) {
            html += `
                    <li>
                        <input type="checkbox" name="qtype" value="${item.id}" id="qtype-${item.qtype_desc}">
                        <label for="qtype-${item.id}">${item.qtype_desc}</label>
                    </li>
                `;
        });
        html += '</ul>';
        area.html(html);
    });
}

function loadChapters(class_id, sem_id) {
    let area = $('#qchapter');
    area.html('');
    if (!class_id || !sem_id || class_id == 0 || sem_id == 0) return;

    area.html('Loading...');
    $.getJSON(`/api/get_chapter/${class_id}/${sem_id}`, function (data) {
        let html = '<ul>';
        html += `
                <li>
                    <input type="checkbox" name="qchapter" value="0" id="qchapter-0">
                    <label for="qchapter-0"><b>ALL Chapters</b></label>
                </li>
            `;
        $.each(data, function (i, item) {
            html += `
                    <li>
                        <input type="checkbox" name="qchapter" value="${item.id}" id="${item.id}">
                        <label for="qchapter-${item.id}">${item.ch_desc}</label>
                    </li>
                `;
        });
        html += '</ul>';
        area.html(html);
    });
}