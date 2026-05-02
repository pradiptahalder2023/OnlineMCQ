const selectElement = document.getElementById('smclass');

document.addEventListener('DOMContentLoaded', function () {
    receivedData.forEach(item => {
        const option = document.createElement('option');
        option.value = item.value; // Set the option's value
        option.textContent = item.text; // Set the option's visible text
        selectElement.appendChild(option); // Add the option to the select element
    });

});
