let flight_choose = document.getElementById("flight-choose");
let allowedDates = document.getElementById('allowedDates').value.replace(/-/g, '/').split(',');
const button_bookNow = document.getElementById("button_bookNow");

button_bookNow.addEventListener('click', function (event) {
    const timeString = flight_choose.value;
    const date = new Date(timeString);
    const year = date.getFullYear();
    const month = ("0" + (date.getMonth() + 1)).slice(-2);
    const day = ("0" + date.getDate()).slice(-2);
    const formattedDateString = `${year}/${month}/${day}`;

    if(!allowedDates.includes(formattedDateString)){
        event.preventDefault();
        alert("There is no flight at this time, please choose another date");
    }
})