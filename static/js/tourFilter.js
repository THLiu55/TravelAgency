// noinspection JSUnresolvedFunction,JSUnresolvedVariable,DuplicatedCode
// noinspection JSUnresolvedVariable
let min = 1500;
let max = 5000;

// noinspection JSUnresolvedFunction
function tour_filter(duration, min1, max1) {
    checkbox_protect(duration);
    const checkboxes = document.querySelectorAll('input[name="activity-type"]');
    const selectedValues = [];

    checkboxes.forEach((checkbox) => {
    if (checkbox.checked) {
        selectedValues.push(checkbox.value);}
    });


    let activityPrice = [min,max];

    const checkboxes1 = document.querySelectorAll('input[name="activity-duration"]');
    const selectedValues1 = [];

    checkboxes1.forEach((checkbox) => {
    if (checkbox.checked) {
        selectedValues1.push(checkbox.value);}
    });

    let page = $('#page-ajax').val()

    let sort_by = getSortValue()

    $.ajax({
      url: '../tour/tour_filter',
      type: 'POST',
      data: {
          "type1": selectedValues.toString(),
          "tourPrice": activityPrice.toString(),
          "tourDuration": selectedValues1.toString(),
          "page": page,
          "sort_by": sort_by
      },
        success: function(response) {
        let tours = search_now(response.tours);
        let tourList = $('#row-list-ajax');
        tourList.empty();

        for (let i = 0; i < tours.length; i++) {
            let activity = tours[i];
            let html = '<div class="col-md-6 col-lg-4">' +
                 '<div class="activity-item">' +
                 '<div class="activity-img">' +
                 '<img src="' + activity.images[0] + '" alt="" style="width:500px; height:200px">' +
                 '<a href="' + activity.contact_email + '" class="add-wishlist"><i class="far fa-heart"></i></a>' +
                 '</div>' +
                 '<div class="activity-content">' +
                 '<h4 class="activity-title"><a href="' + activity.contact_email + '">' + activity.name + '</a></h4>' +
                 '<p><i class="far fa-location-dot"></i>' + activity.address + ', ' + activity.city + '</p>' +
                 '<div class="activity-rate">' +
                 '<span class="badge"><i class="fal fa-star"></i>'+ activity.contact_phone +'</span>' +
                 '<span class="activity-rate-type">' + activity.lat + '</span>' +
                 '<span class="activity-rate-review">(' + activity.review_num + ' Reviews)</span>' +
                 '</div>' +
                 '<div class="activity-bottom">' +
                 '<div class="activity-price">' +
                 '<span class="activity-price-amount">$' + activity.price + '</span>' +
                 '</div>' +
                 '<div class="activity-text-btn">' +
                 '<a href="' + activity.contact_email + '">See Details <i class="fas fa-arrow-right"></i></a>' +
                 '</div>' +
                 '</div>' +
                 '</div>' +
                 '</div>' +
                 '</div>';
            tourList.append(html);
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
            tour_filter(3,ui.values[0], ui.values[1]);
        }
    });
});

function checkbox_protect(d) {
    if (d!==3){
        let checkboxes = document.getElementsByName("activity-duration");
        let check;
        check = checkboxes[d].checked === true;
        for (let i = 0; i < checkboxes.length; i++) {
            checkboxes[i].checked = false;
        }
        checkboxes[d].checked = check;
    }
}

function getSortValue() {
    let selectElement = document.querySelector('#sort-select-ajax');
    let index = selectElement.selectedIndex;
    let options = selectElement.options;
    return options[index].value;
}

function search_now(list) {
    const options = {
        threshold: 0.1,
        tokenize:true,
        ignoreCase: true,
        ignoreLocation: true,
        keys: [
            "name",
            "city",
            "state",
            "address",
            "description"
        ]
    };

    let pattern = document.getElementById("search_box_change").value;
    if (pattern === ''){
        return list;
    }


    const fuse = new Fuse(list, options);
    const patterns = pattern.split(',');

    let results = new Set();

    for (let i = 0; i < patterns.length; i++) {
        const currentPattern = patterns[i].trim();
        const searchResults = fuse.search(currentPattern);

        for (let j = 0; j < searchResults.length; j++) {
            results.add(searchResults[j].item);
        }
    }

    return Array.from(results);
}






