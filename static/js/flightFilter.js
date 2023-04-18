// noinspection JSUnresolvedFunction,JSUnresolvedVariable,DuplicatedCode
// noinspection JSUnresolvedVariable
let min = 1500;
let max = 5000;

// noinspection JSUnresolvedFunction
function flight_filter() {
    const checkboxes = document.querySelectorAll('input[name="flight-time"]');
    const selectedValues = [];

    checkboxes.forEach((checkbox) => {
    if (checkbox.checked) {
        selectedValues.push(checkbox.value);}
    });


    let activityPrice = [min,max];

    const checkboxes1 = document.querySelectorAll('input[name="flight-class"]');
    const selectedValues1 = [];

    checkboxes1.forEach((checkbox) => {
    if (checkbox.checked) {
        selectedValues1.push(checkbox.value);}
    });

    alert(selectedValues1);

    const checkboxes2 = document.querySelectorAll('input[name="flight-airline"]');
    const selectedValues2 = [];

    checkboxes2.forEach((checkbox) => {
    if (checkbox.checked) {
        selectedValues2.push(checkbox.value);}
    });

    const checkboxes3 = document.querySelectorAll('input[name="flight-stop"]');
    const selectedValues3 = [];

    checkboxes3.forEach((checkbox) => {
    if (checkbox.checked) {
        selectedValues3.push(checkbox.value);}
    });

    const checkboxes4 = document.querySelectorAll('input[name="flight-refundable"]');
    const selectedValues4 = [];

    checkboxes4.forEach((checkbox) => {
    if (checkbox.checked) {
        selectedValues4.push(checkbox.value);}
    });


    let page = $('#page-ajax').val()

    let sort_by = getSortValue()

    $.ajax({
      url: '../flight/flight_filter',
      type: 'POST',
      data: {
          "dep_time": selectedValues.toString(),
          "class_type": selectedValues1.toString(),
          "flightPrice": activityPrice.toString(),
          "flight-airline": selectedValues2.toString(),
          "flight-stop": selectedValues3.toString(),
          "flight-refundable": selectedValues4.toString(),
          "page": 1,
          "sort_by": sort_by
      },
        success: function(response) {
        let flights = response.flights;
        let flightList = $('#row-list-ajax');
        flightList.empty();

        for (let i = 0; i < flights.length; i++) {
            let flight = flights[i];
            let html = "<div class=\"col-lg-6\">\n" +
                "<div class=\"flight-booking-item\">\n" +
                "<div class=\"flight-booking-wrapper\">\n" +
                "<div class=\"flight-booking-info\">\n" +
                "<div class=\"flight-booking-content\">\n" +
                "<div class=\"flight-booking-airline\">\n" +
                "<div class=\"flight-airline-img\">\n" +
                "<img  src=\"{{ url_for('static', filename=flight.images[0].replace('\\\\','/')) }}\" alt=\"\" style=\"width:500px; height:100px\" >\n" +
                "</div>\n" +
                "<h5 class=\"flight-airline-name\">{{ flight.company }}</h5>\n" +
                "</div>\n" +
                "<div class=\"flight-booking-time\">\n" +
                "<div class=\"start-time\">\n" +
                "<div class=\"start-time-icon\">\n" +
                "<i class=\"fal fa-plane-departure\"></i>\n" +
                "</div>\n" +
                "<div class=\"start-time-info\">\n" +
                "<h6 class=\"start-time-text\">{{flight.takeoff_time}}</h6>\n" +
                "<span class=\"flight-destination\">{{flight.departure}}</span>\n" +
                "</div>\n" +
                "</div>\n" +
                "<div class=\"flight-stop\">\n" +
                "<span class=\"flight-stop-number\">{{flight.flight_stop}}</span>\n" +
                "<div class=\"flight-stop-arrow\"></div>\n" +
                "</div>\n" +
                "<div class=\"end-time\">\n" +
                "<div class=\"start-time-icon\">\n" +
                "<i class=\"fal fa-plane-arrival\"></i>\n" +
                "</div>\n" +
                " <div class=\"start-time-info\">\n" +
                "<h6 class=\"end-time-text\">{{flight.landing_time}}</h6>\n" +
                "<span class=\"flight-destination\">{{flight.destination}}</span>\n" +
                "</div>\n" +
                "</div>\n" +
                "</div>\n" +
                "<div class=\"flight-booking-duration\">\n" +
                "<span class=\"duration-text\">{{flight.total_time}} hour(s)</span>\n" +
                "</div>\n" +
                "</div>\n" +
                "</div>\n" +
                "<div class=\"flight-booking-price\">\n" +
                "<div class=\"price-info\">\n" +
                "<!-- <del class=\"discount-price\">$5,548</del> -->\n" +
                "<span class=\"price-amount\">{{flight.price}}</span>\n" +
                "</div>\n" +
                "<a href=\"{{ url_for('flight.flightDetail', flight_id=flight.id) }}\" class=\"theme-btn\">Book Now<i class=\"far fa-arrow-right\"></i></a>\n" +
                "</div>\n" +
                "</div>\n" +
                "<div class=\"flight-booking-detail\">\n" +
                "<div class=\"flight-booking-detail-header\">\n" +
                "<p>{{flight.fare_type}}</p>\n" +
                "</div>\n" +
                "</div>\n" +
                "</div>\n" +
                "</div>"

            flightList.append(html);
        }},
    });
}

$(function() {
    $("#price-range1").slider({
        // 设置滑块的最小值、最大值、初始值等参数
        min: 0,
        max: 10000,
        values: [1500, 5000],
        // 滑块停止拖动时触发的函数
        stop: function(event, ui) {
            min = ui.values[0];
            max = ui.values[1];
            flight_filter();
        }
    });
});

function getSortValue() {
    let selectElement = document.querySelector('#sort-select-ajax');
    let index = selectElement.selectedIndex;
    let options = selectElement.options;
    return options[index].value;
}