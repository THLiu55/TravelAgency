let first_date = document.getElementById("journey-date");
let end_date = document.getElementById("return-date");
const button_bookNow = document.getElementById("button-cancel");

button_bookNow.addEventListener('click', function (event) {
    let allowedDates = document.getElementById('allowedDates').value.replace(/-/g, '/').split(',');
    const timeString0 = first_date.value;
    const date0 = new Date(timeString0);
    const year0 = date0.getFullYear();
    const month0 = ("0" + (date0.getMonth() + 1)).slice(-2);
    const day0 = ("0" + date0.getDate()).slice(-2);
    const formattedDateString0 = `${year0}/${month0}/${day0}`;

    const timeString = end_date.value;
    const date = new Date(timeString);
    const year = date.getFullYear();
    const month = ("0" + (date.getMonth() + 1)).slice(-2);
    const day = ("0" + date.getDate()).slice(-2);
    const formattedDateString = `${year}/${month}/${day}`;

    if (allowedDates.indexOf(formattedDateString0)>allowedDates.indexOf(formattedDateString)){
        alert("The check-in date must be no later than the check out date");
        event.preventDefault();
    }

})