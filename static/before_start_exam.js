const days = document.getElementById("days");
const hrs = document.getElementById("hrs");
const mins = document.getElementById("mins");
const secs = document.getElementById("secs");

const divCountdown = document.querySelector('.coundown-container')

// on page load 
document.addEventListener("DOMContentLoaded", function () {

    // retrives scheduled datetime
    examInfo = receivedData
    const isoDateString = examInfo[0]['Schedule']
    const examtimedomain = examInfo[0]['ExamTimeDomain']
    const dateObject = new Date(isoDateString);
    const scheduledDatetime = dateObject.toLocaleString();
    const sch_datetime = new Date(scheduledDatetime)

    // constructs current datetime
    const myDate = new Date();
    const currentDatetime = myDate.toLocaleString();
    const cur_datetime = new Date(currentDatetime);
    const diffInMilliseconds = sch_datetime - cur_datetime;

    // check if already submitted
    if (exam_status[0]['stat'] === "Yes") {
        alert("Sorry...You have already submitted the Question Paper");

        //disables start button
        disableStartBtn();

        // now redirect to dashboaed
        const targetUrl = `/dashboard_user`;
        window.location.href = targetUrl;
    }
    else {
        if (diffInMilliseconds > 0) {
            // display countdown countdown div
            divCountdown.style.display = "flex"
            divCountdown.classList.add('coundown-containercss')

            //disables start button
            disableStartBtn();

            //starts countdown
            startTimer(sch_datetime);
        }
        else {
            // const diffInMinutes = Math.abs(diffInMilliseconds / (1000 * 60));
            const diffInMinutes = Math.abs((diffInMilliseconds / 1000) / 60);
           
            if (diffInMinutes < Number(examtimedomain)) {
                // do nothing
            }
            else {
                alert("Sorry! .. Exam has Expired");

                //disables start button
                disableStartBtn();


                // now redirect to dashboaed
                const targetUrl = `/dashboard_user`;
                window.location.href = targetUrl;
            }
        }
    }



})

// Function to Show Alert
// const displayAlert = (msg) => {
//     alert.style.display = "block";
//     alert.textContent = msg;
//     setTimeout(()=>{
//         alert.style.display = "none";
//     }, 2000);
// }

// Function to Start Timer
const startTimer = (sch_datetime) => {

    const countdownInterval = setInterval(function () {
        const now = new Date().getTime();
        const timeDifference = sch_datetime - now;

        //converts milliseconds to hrs, mins, secs
        const calcSecs = Math.floor(timeDifference / 1000) % 60; // % remainder operator
        const calcMins = Math.floor(timeDifference / 1000 / 60) % 60;
        const calcHours = Math.floor(timeDifference / 1000 / 60 / 60) % 24;
        const calcDays = Math.floor(timeDifference / 1000 / 60 / 60 / 24);

        days.textContent = formatTime(calcDays);
        hrs.textContent = formatTime(calcHours);
        mins.textContent = formatTime(calcMins);
        secs.textContent = formatTime(calcSecs);

        if (timeDifference < 0) {
            clearInterval(countdownInterval);

            // Enables start link button;
            enableStartBtn();

            // set display countdown div to none
            divCountdown.style.display = "none"
        }

    }, 1000);
}

const formatTime = (time) => {
    return time < 10 ? `0${time}` : time;
}

//disables the start link button
function disableStartBtn() {
    const startbtn = document.getElementById('startExam');

    // set href to '#' or 'javascript:void(0);' to prevent navigation
    startbtn.href = '#';
    // myLink.href = 'javascript:void(0);'; .

    // Optionally, style it to appear disabled
    startbtn.style.color = 'gray';
    startbtn.style.cursor = 'default';
}

function enableStartBtn() {
    const startbtn = document.getElementById('startExam');

    // Restores the href attribute
    startbtn.href = "/exam/start_exam";

    // Optionally, style it to appear disabled
    startbtn.style.color = '';
    startbtn.style.cursor = '';
}