function select_one(item){
    item = parseInt(item);
    let checkboxes = document.getElementsByName("room-select");
    for (let i = 0; i < checkboxes.length; i++) {
            checkboxes[i].checked = false;
    }
    checkboxes[item].checked = true;
}

document.addEventListener("DOMContentLoaded", function() {
    const button = document.getElementById("button-cancel");
    button.addEventListener("click", function(event) {
        let checkboxes = document.getElementsByName("room-select");
        let item;
        for (let i = 0; i < checkboxes.length; i++) {
            if(checkboxes[i].checked === true){
                item = checkboxes[i]
            }
        }
        if(typeof(item) === "undefined"){
            alert("Please choose a room type")
            event.preventDefault();
        }else {
            let startDate = new Date(document.getElementById("journey-date").value);
            let endDate = new Date(document.getElementById("return-date").value);
            let diff = endDate.getTime() - startDate.getTime();
            let days_span = (diff / (1000 * 3600 * 24)) + 1;

            let days = parseInt(button.value)

            if (days===2){
                if (days_span>2){
                    alert("Please change the check-in time to two days or less");
                    event.preventDefault();
                }else{
                    const arr = item.value.split(";");
                    const beforeSemicolon = parseFloat(arr[0]);
                    document.getElementById("to-submit-roomID").value=arr[1];
                    document.getElementById("to-submit-price").value= beforeSemicolon*days_span;
                }
            }else{
                if (days_span<3){
                    alert("Please change the check-in time to three days or more");
                    event.preventDefault();
                }else {
                    const arr = item.value.split(";");
                    const beforeSemicolon = parseFloat(arr[0]);
                    document.getElementById("to-submit-roomID").value=arr[1];
                    document.getElementById("to-submit-price").value= beforeSemicolon*days_span;
                }
            }


        }
    });
});