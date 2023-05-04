let cur_status = "All Status"
let cur_category = "All Category"
const item_container = document.getElementById("item-container")
const modifyProduct = document.getElementById("modifyProduct")
let BASE_URL = window.location.origin

function load_hotels(published, category) {
    if (published == null) {
        published = cur_status
    }
    if (category == null) {
        category = cur_category
    }
    cur_category = category
    cur_status = published
    console.log("here")
    console.log(BASE_URL)
    let xhr = new XMLHttpRequest()
    const fd = new FormData()
    fd.set('publish', published)
    fd.set('category', category)
    xhr.open('POST', '/manager/load_hotels', true)
    xhr.send(fd)

    // set animation after email send / error notification for registered email
    xhr.onload = function() {
        items = JSON.parse(xhr.responseText)['content']
        item_container.innerHTML = ''
        for (let i = 0; i < items.length; i++) {
            let tr = document.createElement("tr");
            tr.className = "table__row";
            status_img = ``
            if (items[i]['status'] === "published") {
                status_img = `<div class="table__status"><span class="table__status-icon color-green"></span>
                                        ${items[i].status}
                                    </div>`
            } else {
                status_img = `<div class="table__status"><span class="table__status-icon color-red"></span>
                                        ${items[i].status}
                                    </div>`
            }
            s = `<tr class="table__row">
                                <td class="table__td">
                                    <div class="table__checkbox table__checkbox--all">
                                        <label class="checkbox">
                                            <input type="checkbox" data-checkbox="product"><span
                                                class="checkbox__marker"><span class="checkbox__marker-icon">
                                                    <svg class="icon-icon-checked">
                                                        <use xlink:href="#icon-checked"></use>
                                                    </svg></span></span>
                                        </label>
                                    </div>
                                </td>
                                <td class="d-none d-lg-table-cell table__td"><span class="text-grey">${items[i].id}</span>
                                </td>
                                <td class="table__td">${items[i].name}</td>
                                <td class="table__td"><span class="text-grey">${items[i].room_num}</span>
                                </td>
                                <td class="table__td"><span>${items[i].price}</span>
                                </td>
                                <td class="d-none d-lg-table-cell table__td"><span
                                        class="text-grey">${items[i].city}</span>
                                </td>
                                <td class="d-none d-sm-table-cell table__td">
                                    ${status_img}
                                </td>
                                <td class="table__td table__actions">
                                    <div class="items-more">
                                        <button class="items-more__button">
                                            <svg class="icon-icon-more">
                                                <use xlink:href="#icon-more"></use>
                                            </svg>
                                        </button>
                                        <div class="dropdown-items dropdown-items--right">
                                            <div class="dropdown-items__container">
                                                <ul class="dropdown-items__list">
                                                    <li class="dropdown-items__item">
                                                        <a class="dropdown-items__link" onclick="getModifyData(${items[i].id})">
                                                            <span class="dropdown-items__link-icon" onclick="modify(${items[i].id})" style="padding-left: 50%;">
                                                                <button id="button_Modify" style="max-width: 100px;max-height: 30px; white-space: nowrap;">
                                                                <svg class="icon-icon-view" style="max-width: 60px;max-height: 10px;">
                                                                    <use xlink:href="#icon-view"></use>
                                                                </svg>Modify
                                                                </button>
                                                            </span>
                                                        </a>
                                                    </li>
                                                    <li class="dropdown-items__item" >
                                                        <a class="dropdown-items__link" onclick="delete_item(${items[i].id})">
                                                        <span class="dropdown-items__link-icon" style="padding-left: 50%;">
                                                                <button data-modal="#deleteProduct" style="max-width: 100px;max-height: 30px;  white-space: nowrap;">
                                                                <svg class="icon-icon-trash">
                                                                    <use xlink:href="#icon-trash"></use>
                                                                </svg>Delete
                                                            </button>
                                                        </span>
                                                        </a>
                                                    </li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </td>
                            </tr>`
            tr.innerHTML = s
            item_container.appendChild(tr)
        }

                const button_Modify = document.querySelectorAll("#button_Modify")

        // for (let i = 1; i < button_Modify.length; i++) {
        //
        // }
        button_Modify.forEach(item => {
            item.addEventListener('click', () => {
                modifyProduct.classList.add("is-active", "is-animate")
            })
        })
    }
}

load_hotels(cur_status, cur_category)

function delete_item(id) {
    let xhr = new XMLHttpRequest()
    const fd = new FormData()
    fd.set('id', id)
    xhr.open('POST', '/manager/delete_hotel', true)
    xhr.send(fd)

    // set animation after email send / error notification for registered email
    xhr.onload = function() {
        load_hotels(cur_status, cur_category)
    }
}

function clearInputs(){
    location.reload();
}

function setModifySelect(id,value) {
    const select = $("#"+id);
    select.val(value)
    select.niceSelect("update");
}

function initRoomType(init_num){
    // {#  modify dynamic itinerary  #}
    $("#divRoomContainer_modify").empty();
    for (var i = 0; i < init_num; i++) {
        var formGroup = $('<div class="form-group"></div>');
        var labelname = $('<label for="hotelroom_name_' + i + '">Room Name - Room Type' + i + '</label>');
        var inputname = $('<input name="hotelroom_name_' + i + '" type="text" class="form-control" placeholder="Enter room name">');

        var inputformGroup = $('<div class="input-form-group" style="display: grid;grid-template-columns: 1fr 1fr 1fr;justify-items: start;margin-left: 5%;margin-top:2%;"></div>');
        var labelWifi = $('<div style="display:grid;"><label class="form-check-label" for="hotelroom_wifi_' + i + '">Wifi</label></div>');
        var checkboxWifi = $('<input name="feature_1_' + i + '" type="checkbox" class="form-check-input" value="WiFi" style="-webkit-appearance:checkbox;">');

        var labelBed = $('<div style="display:grid;"><label class="form-check-label" for="hotelroom_1bed_' + i + '">1 Single bed</label></div>');
        var checkboxBed = $('<input name="feature_2_' + i + '" type="checkbox" class="form-check-input" value="1 Single bed" style="-webkit-appearance:checkbox;">');

        var label2Beds = $('<div style="display:grid;"><label class="form-check-label" for="hotelroom_2bed_' + i + '">2 Single beds</label></div>');
        var checkbox2Beds = $('<input name="feature_3_' + i + '" type="checkbox" class="form-check-input" value="2 single beds" style="-webkit-appearance:checkbox;">');

        var labelRoomArea15 = $('<div style="display:grid;"><label class="form-check-label" for="hotelroom_Area15_' + i + '">15 ㎡</label></div>');
        var checkboxRoomArea15 = $('<input name="feature_4_' + i + '" type="checkbox" class="form-check-input" value="15 ㎡" style="-webkit-appearance:checkbox;">');

        var labelRoomArea25 = $('<div style="display:grid;"><label class="form-check-label" for="hotelroom_Area25_' + i + '">25 ㎡</label></div>');
        var checkboxRoomArea25 = $('<input name="feature_5_' + i + '" type="checkbox" class="form-check-input" value="25 ㎡" style="-webkit-appearance:checkbox;">');

        var labelBath = $('<div style="display:grid;"><label class="form-check-label" for="hotelroom_Bath_' + i + '">Shower And Bathtub</label></div>');
        var checkboxBath = $('<input name="feature_6_' + i + '" type="checkbox" class="form-check-input" value="Shower And Bathtub" style="-webkit-appearance:checkbox;">');

        var labelToiletries = $('<div style="display:grid;"><label class="form-check-label" for="hotelroom_Toiletries_' + i + '">Free Toiletries</label></div>');
        var checkboxToiletries = $('<input name="feature_7_' + i + '" type="checkbox" class="form-check-input" value="Free Toiletries" style="-webkit-appearance:checkbox;">');

        var labelprice = $('<label for="hotelroom_price_' + i + '">Room Price</label>');
        var inputprice = $('<input name="hotelroom_price_' + i + '" type="number" min=0 class="form-control" placeholder="Enter room price">');
        var label = $('<label for="fileInput' + i + '"></label>');
        var customFile = $('<div class="custom-file"></div>');
        var fileInput = $('<input type="file" class="custom-file-input" name="fileInput' + i + '" id="fileInput' + i + '" style="display:none;">');
        var fileLabel = $('<label class="custom-file-label" for="fileInput' + i + '" style="margin-top:20px; border-radius:10px;">Upload pictures</label>');
        var fileNameInput = $('<input type="text" class="form-control" id="fileNameInput' + i + '" style="display:none;" readonly>');

        // 将文件名显示在对应的文本框中
        fileInput.on("change", function () {
            var fileName = $(this).val().split("\\").pop();
            var index = $(this).attr("id").match(/\d+/)[0]; // 提取文件上传控件的索引号
            $("#fileNameInput" + index).val(fileName);
            $(this).next(".custom-file-label").html(fileName);
        });


        customFile.append(fileInput);
        customFile.append(fileLabel);
        formGroup.append(labelname);
        formGroup.append(inputname);

        // inputformGroup.append(checkboxWifi);
        labelWifi.append(checkboxWifi);
        inputformGroup.append(labelWifi);


        // inputformGroup.append(checkboxBed);
        labelBed.append(checkboxBed);
        inputformGroup.append(labelBed);


        label2Beds.append(checkbox2Beds);
        // inputformGroup.append(checkbox2Beds);
        inputformGroup.append(label2Beds);


        // inputformGroup.append(checkboxRoomArea15);
        labelRoomArea15.append(checkboxRoomArea15);
        inputformGroup.append(labelRoomArea15);


        // inputformGroup.append(checkboxRoomArea25);
        labelRoomArea25.append(checkboxRoomArea25);
        inputformGroup.append(labelRoomArea25);


        // inputformGroup.append(checkboxBath);
        labelBath.append(checkboxBath);
        inputformGroup.append(labelBath);


        // inputformGroup.append(checkboxToiletries);
        labelToiletries.append(checkboxToiletries);
        inputformGroup.append(labelToiletries);
        formGroup.append(inputformGroup);
        formGroup.append(labelprice);
        formGroup.append(inputprice);
        formGroup.append(label);
        formGroup.append(customFile);
        formGroup.append(fileNameInput);

        $("#divRoomContainer_modify").append(formGroup);
    }

}

function checkedInitIncluded(checked_array){
    var incheck1 = document.getElementById('m_included1');
    if (checked_array.includes(incheck1.value)){
        incheck1.checked = true;
    }else {
        incheck1.checked = false;
    }

    var incheck2 = document.getElementById('m_included2');
    if (checked_array.includes(incheck2.value)){
        incheck2.checked = true;
    }else {
        incheck2.checked = false;
    }

    var incheck3 = document.getElementById('m_included3');
    if (checked_array.includes(incheck3.value)){
        incheck3.checked = true;
    }else {
        incheck3.checked = false;
    }

    var incheck4 = document.getElementById('m_included4');
    if (checked_array.includes(incheck4.value)){
        incheck4.checked = true;
    }else {
        incheck4.checked = false;
    }

    var incheck5 = document.getElementById('m_included5');
    if (checked_array.includes(incheck5.value)){
        incheck5.checked = true;
    }else {
        incheck5.checked = false;
    }

    var incheck6 = document.getElementById('m_included6');
    if (checked_array.includes(incheck6.value)){
        incheck6.checked = true;
    }else {
        incheck6.checked = false;
    }

    var incheck7 = document.getElementById('m_included7');
    if (checked_array.includes(incheck7.value)){
        incheck7.checked = true;
    }else {
        incheck7.checked = false;
    }

    var incheck8 = document.getElementById('m_included8');
    if (checked_array.includes(incheck8.value)){
        incheck8.checked = true;
    }else {
        incheck8.checked = false;
    }

    var incheck9 = document.getElementById('m_included9');
    if (checked_array.includes(incheck9.value)){
        incheck9.checked = true;
    }else {
        incheck9.checked = false;
    }

    var incheck10 = document.getElementById('m_included10');
    if (checked_array.includes(incheck10.value)){
        incheck10.checked = true;
    }else {
        incheck10.checked = false;
    }

    var incheck11 = document.getElementById('m_included11');
    if (checked_array.includes(incheck11.value)){
        incheck11.checked = true;
    }else {
        incheck11.checked = false;
    }

    var incheck12 = document.getElementById('m_included12');
    if (checked_array.includes(incheck12.value)){
        incheck12.checked = true;
    }else {
        incheck12.checked = false;
    }

    var incheck13 = document.getElementById('m_included13');
    if (checked_array.includes(incheck13.value)){
        incheck13.checked = true;
    }else {
        incheck13.checked = false;
    }

    var incheck14 = document.getElementById('m_included14');
    if (checked_array.includes(incheck14.value)){
        incheck14.checked = true;
    }else {
        incheck14.checked = false;
    }

    var incheck15 = document.getElementById('m_included15');
    if (checked_array.includes(incheck15.value)){
        incheck15.checked = true;
    }else {
        incheck15.checked = false;
    }

    var incheck16 = document.getElementById('m_included16');
    if (checked_array.includes(incheck16.value)){
        incheck16.checked = true;
    }else {
        incheck16.checked = false;
    }

    var incheck17 = document.getElementById('m_included17');
    if (checked_array.includes(incheck17.value)){
        incheck17.checked = true;
    }else {
        incheck17.checked = false;
    }

    var incheck18 = document.getElementById('m_included18');
    if (checked_array.includes(incheck18.value)){
        incheck18.checked = true;
    }else {
        incheck18.checked = false;
    }

    var incheck19 = document.getElementById('m_included19');
    if (checked_array.includes(incheck19.value)){
        incheck19.checked = true;
    }else {
        incheck19.checked = false;
    }

    var incheck20 = document.getElementById('m_included20');
    if (checked_array.includes(incheck20.value)){
        incheck20.checked = true;
    }else {
        incheck20.checked = false;
    }
}

function getModifyData(id){
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
       if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
        // 处理服务器返回的数据
            console.log(response);
            //参数为设置的id和传入的值（值需要与select中option的value一致）
            setModifySelect("modify_hotel_star", response['content']["hotel_star"]);
            setModifySelect("modify_min_stay", response['content']["min_stay"]);
            setModifySelect("modify_security", response['content']["security"]);
            setModifySelect("modify_on_site_staff", response['content']["on_site_staff"]);
            setModifySelect("modify_house_keeping", response['content']["house_keeping"]);
            setModifySelect("modify_front_desk", response['content']["front_desk"]);
            setModifySelect("modify_bathroom", response['content']["bathroom"]);

            setModifySelect("m_name", response['content']["name"]);
            setModifySelect("m_room_num", response['content']["room_num"]);
            setModifySelect("m_min_price", response['content']["min_price"]);
            setModifySelect("m_city", response['content']["city"]);
            setModifySelect("m_state", response['content']["state"]);
            setModifySelect("m_description", response['content']["description"]);
            setModifySelect("m_contact_name", response['content']["contact_name"]);
            setModifySelect("m_email", response['content']["contact_email"]);
            setModifySelect("m_phone", response['content']["contact_phone"]);
            setModifySelect("inputRoomNumber_modify", response['content']["room_type_num"]);

            setModifySelect('m_pri', response['content']["pri"]);

            initRoomType(response['content']["room_type_num"])

            const tick_array = response['content']["amenities"]
            checkedInitIncluded(tick_array)
        } else {
        // 处理错误情况
            console.log('wrong');
        }
      }
    };
    xhr.open('POST', '/manager/load_info');
    const fd = new FormData()
    fd.set('id', id)
    fd.set('type', "hotel")
    xhr.send(fd);
}