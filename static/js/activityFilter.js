// noinspection JSUnresolvedFunction,JSUnresolvedVariable,DuplicatedCode
// noinspection JSUnresolvedVariable
let min = 1500;
let max = 5000;

// noinspection JSUnresolvedFunction
function activity_filter(duration, min1, max1) {
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
      url: '../activity/activity_filter',
      type: 'POST',
      data: {
          "type1": selectedValues.toString(),
          "activityPrice": activityPrice.toString(),
          "activityDuration": selectedValues1.toString(),
          "page": page,
          "sort_by": sort_by
      },
        success: function(response) {
        let activities = response.activities;
        let activityList = $('#row-list-ajax');
        activityList.empty();

        for (let i = 0; i < activities.length; i++) {
            let activity = activities[i];
            let html = '<div class="col-md-6 col-lg-4">' +
                 '<div class="activity-item">' +
                 '<div class="activity-img">' +
                 '<img src="' + activity.images[0] + '" alt="" style="width:500px; height:200px">' +
                 '<a href="#" class="add-wishlist"><i class="far fa-heart"></i></a>' +
                 '</div>' +
                 '<div class="activity-content">' +
                 '<h4 class="activity-title"><a href="#">' + activity.name + '</a></h4>' +
                 '<p><i class="far fa-location-dot"></i>' + activity.address + ', ' + activity.city + '</p>' +
                 '<div class="activity-rate">' +
                 '<span class="badge"><i class="fal fa-star"></i> 5.0</span>' +
                 '<span class="activity-rate-type">Excellent</span>' +
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
            activityList.append(html);
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
            activity_filter(3,ui.values[0], ui.values[1]);
        }
    });
});

function checkbox_protect(d) {
    if (d!==3){
        let checkboxes = document.getElementsByName("activity-duration");
        for (let i = 0; i < checkboxes.length; i++) {
            checkboxes[i].checked = false;
        }
        checkboxes[d].checked = true;
    }
}

function getSortValue() {
    let selectElement = document.querySelector('#sort-select-ajax');
    let index = selectElement.selectedIndex;
    let options = selectElement.options;
    return options[index].value;
}






