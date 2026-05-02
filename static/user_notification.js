notifications = receivedData;

document.addEventListener('DOMContentLoaded', function () {
    // Your JavaScript code to execute after the DOM is loaded goes here
    for (i = 0; i < notifications.length; i++) {
        let spanid = "a" + (i + 1)
        let myElement = document.getElementById(spanid);
        if (myElement) {
            myElement.innerText = setElapsedTime(notifications[i].createdon);
        }
    }

});

function setElapsedTime(createdon) {
    const startDate = new Date(createdon);
    const endDate = new Date();

    const startTimeInMs = startDate.getTime();
    const endTimeInMs = endDate.getTime();

    const differenceInMs = endTimeInMs - startTimeInMs;

    let differenceInDays = Math.round(differenceInMs / (1000 * 60 * 60 * 24));
    let differenceInHours = Math.round(differenceInMs / (1000 * 60 * 60));
    let differenceInMinutes = Math.round(differenceInMs / (1000 * 60));
    let differenceInSeconds = Math.round(differenceInMs / 1000);

    if (differenceInDays >= 1) {
        return String(differenceInDays) + " days ago";
    }
    else if (differenceInHours >= 1) {
        return String(differenceInHours) + " hrs ago";
    }
    else if (differenceInMinutes >= 1) {
        return String(differenceInMinutes) + " minutes ago";
    }
    else {
        return String(differenceInSeconds) + " sec ago";
    }
}

