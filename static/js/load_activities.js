let cur_status = "All Status"
let cur_category = "All Category"
const item_container = document.getElementById("item-container")
const modifyProduct = document.getElementById("modifyProduct")
const modify_form = document.getElementById("modify_form")
let BASE_URL = window.location.origin

console.log(modifyProduct)
function load_activities(published, category) {
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
    xhr.open('POST', '/manager/load_activities', true)
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
                                <td class="table__td"><span class="text-grey">${items[i].category}</span>
                                </td>
                                <td class="table__td"><span>${items[i].price}</span>
                                </td>
                                <td class="d-none d-lg-table-cell table__td"><span
                                        class="text-grey">${items[i].start_time}</span>
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
                                                                <span class="dropdown-items__link-icon" style="padding-left: 50%;">
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

load_activities(cur_status, cur_category)

function delete_item(id) {
    let xhr = new XMLHttpRequest()
    const fd = new FormData()
    fd.set('id', id)
    xhr.open('POST', '/manager/delete_activity', true)
    xhr.send(fd)

    // set animation after email send / error notification for registered email
    xhr.onload = function() {
        load_activities(cur_status, cur_category)
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

function checkedInitIncluded(checked_array){
    var incheck1 = document.getElementById('m_included1');
    if (checked_array[0] != null){
        incheck1.checked = true;
    }else {
        incheck1.checked = false;
    }

    var incheck2 = document.getElementById('m_included2');
    if (checked_array[1] != null){
        incheck2.checked = true;
    }else {
        incheck2.checked = false;
    }

    var incheck3 = document.getElementById('m_included3');
    if (checked_array[2] != null){
        incheck3.checked = true;
    }else {
        incheck3.checked = false;
    }

    var incheck4 = document.getElementById('m_included4');
    if (checked_array[3] != null){
        incheck4.checked = true;
    }else {
        incheck4.checked = false;
    }
}

function checkedInitNotIncluded(checked_array){
    var incheck1 = document.getElementById('m_not-included1');
    if (checked_array[0] != null){
        incheck1.checked = true;
    }else {
        incheck1.checked = false;
    }

    var incheck2 = document.getElementById('m_not-included2');
    if (checked_array[1] != null){
        incheck2.checked = true;
    }else {
        incheck2.checked = false;
    }

    var incheck3 = document.getElementById('m_not-included3');
    if (checked_array[2] != null){
        incheck3.checked = true;
    }else {
        incheck3.checked = false;
    }

    var incheck4 = document.getElementById('m_not-included4');
    if (checked_array[3] != null){
        incheck4.checked = true;
    }else {
        incheck4.checked = false;
    }
}


function getModifyData(id){
    var xhr = new XMLHttpRequest();
    modify_form.action = `/manager/modify_activity?id=${id}`
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
       if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
        // 处理服务器返回的数据
            console.log(response['content']);
            //参数为设置的id和传入的值（值需要与select中option的value一致）
            setModifySelect("modify_Activity_Category", response['content']["category"]);
            setModifySelect("modify_Duration", response['content']["duration"]);
            setModifySelect("modify_group_size", response['content']["group_size"]);

            // setModifySelect('modify_name', response['content']["name"];
            setModifySelect("modify_name", response['content']["name"]);
            setModifySelect('modify_Price', response['content']["price"]);
            setModifySelect('modify_city', response['content']["city"]);
            setModifySelect('modify_state', response['content']["state"]);
            setModifySelect('modify_address', response['content']["address"]);
            setModifySelect('m_visitHour', response['content']["visitHour"]);
            setModifySelect('m_contact_name', response['content']["contact_name"]);
            setModifySelect('m_contact_email', response['content']["contact_email"]);
            setModifySelect('m_contact_phone', response['content']["contact_phone"]);
            setModifySelect('m_description', response['content']["description"]);
            setModifySelect('modify_citylong', response['content']['lon'])
            setModifySelect('modify_citylati', response['content']['lat'])

            setModifySelect('m_pri', response['content']["pri"]);

            var datePicker1 = document.getElementById('m_from_date');
            start_time = response['content']["start_time"]
            date_str1 = start_time.split(" ")[0]
            console.log(date_str1)
            datePicker1.value = date_str1;

            var datePicker2 = document.getElementById('m_end_date');
            end_time = response['content']["end_time"]
            date_str2 = end_time.split(" ")[0]
            console.log(date_str2)
            datePicker2.value = date_str2;

            var datePicker3 = document.getElementById('m_open_hour');
            open_hour = response['content']["openHour"]
            datePicker3.value = open_hour;

            const tick_array = JSON.parse(response['content']["included"])
            const tick_array_not = JSON.parse(response["content"]["excluded"])
            checkedInitIncluded(tick_array.included)
            checkedInitNotIncluded(tick_array_not.not_included)

        } else {
        // 处理错误情况
            console.log('wrong');
        }
      }
    };
    xhr.open('POST', '/manager/load_info');
    const fd = new FormData()
    fd.set('id', id)
    fd.set('type', "activity")
    xhr.send(fd);
}