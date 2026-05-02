// on load of the form
document.addEventListener('DOMContentLoaded', function () {

    // sets the value in class select box
    document.getElementById('smclass').value = receivedData[0].smclass;

    // sets the value in option1 input box
    document.getElementById('smdesc').value = receivedData[0].smdesc;

});

