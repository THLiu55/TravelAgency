let cur_status = "All Status"
let cur_category = "All Category"
let cur_pattern = ''
const modify_form = document.getElementById("modify_form")
const item_container = document.getElementById("tour-container")
const modifyProduct = document.getElementById("modifyProduct")
const search_box = document.getElementById("search_box")
let BASE_URL = window.location.origin

function search_tours() {
    let q = search_box.value
    load_tours(null, null, q)
}

function load_tours(published, category, pattern=null) {
    if (published == null) {
        published = cur_status
    }
    if (category == null) {
        category = cur_category
    }
    if (pattern == null) {
        pattern = cur_pattern
    }
    cur_category = category
    cur_status = published
    cur_pattern = pattern
    let xhr = new XMLHttpRequest()
    const fd = new FormData()
    fd.set('publish', published)
    fd.set('category', category)
    xhr.open('POST', '/manager/load_tours', true)
    xhr.send(fd)

    // set animation after email send / error notification for registered email
    xhr.onload = function() {
        items = JSON.parse(xhr.responseText)['content']
        item_container.innerHTML = ''
        items = search_now(items, cur_pattern)
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

load_tours(cur_status, cur_category)

function delete_item(id) {
    let xhr = new XMLHttpRequest()
    const fd = new FormData()
    fd.set('id', id)
    xhr.open('POST', '/manager/delete_tour', true)
    xhr.send(fd)

    // set animation after email send / error notification for registered email
    xhr.onload = function() {
        load_tours(cur_status, cur_category)
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

function initItinerary(init_num){
    // {#  modify dynamic itinerary  #}
    var container_modify = document.getElementById("divContainer_modify");
    // {# initialize #}
    container_modify.innerHTML = "";
    console.log(init_num)
    for (var i = 0; i < init_num; i++) {
        console.log(i)
        var div = document.createElement("div");
        div.innerHTML = "<div class='col-lg-12'><div class='form-group'><label>"+"Itinerary Name" + " - DAY"+(i+1) + "</label><input name='itinerary_name_" + (i+1) + "' type='text' class='form-control' placeholder='Enter itinerary name'></div></div> <div class='col-lg-12'><div class='form-group'><label>Itinerary Description</label><textarea name='itinerary_desc_" + (i+1) + "' class='form-control' placeholder='Write itinerary description' cols='30' rows='5'></textarea></div></div>"
        container_modify.appendChild(div);
    }
}

function getModifyData(id){
    modify_form.action = `/manager/modify_tour?id=${id}`
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
       if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
        // 处理服务器返回的数据
            console.log(response);
            //参数为设置的id和传入的值（值需要与select中option的value一致）
            setModifySelect("modify_category", response['content']["category"]);
            setModifySelect("modify_group_size", response['content']["group_size"]);


            setModifySelect("m_name", response['content']["name"]);
            setModifySelect("m_price", response['content']["price"]);
            setModifySelect("m_city", response['content']["city"]);
            setModifySelect("m_state", response['content']["state"]);
            setModifySelect("m_address", response['content']["address"]);
            setModifySelect("inputNumber_modify", response['content']["duration"]);
            setModifySelect('m_contact_name', response['content']["contact_name"]);
            setModifySelect('m_contact_email', response['content']["contact_email"]);
            setModifySelect('m_contact_phone', response['content']["contact_phone"]);
            setModifySelect('m_description', response['content']["description"]);

            setModifySelect('modify_citylong', response['content']['lon'])
            setModifySelect('modify_citylati', response['content']['lat'])

            setModifySelect('m_pri', response['content']["pri"]);

            const init_num = parseInt(response['content']["duration"])
            initItinerary(init_num)

            const tick_array = JSON.parse(response['content']["included"])
            const tick_array_not = JSON.parse(response["content"]["excluded"])
            checkedInitIncluded(tick_array.included)
            checkedInitNotIncluded(tick_array_not.not_included)

           function convertToDateString(timestamp) {
                const date = new Date(timestamp);
                const dateString = date.toISOString().substring(0, 10);  // 截取字符串获取日期部分，即"2023-05-21"
                return dateString;
            }

           var datePicker1 = document.getElementById('m_from_date');
            start_time = response['content']["start_time"]
            date_str1 = convertToDateString(start_time);
            console.log(date_str1)
            datePicker1.value = date_str1;

            var datePicker2 = document.getElementById('m_end_date');
            end_time = response['content']["end_time"]
            date_str2 = convertToDateString(end_time);
            console.log(date_str2)
            datePicker2.value = date_str2;

        } else {
        // 处理错误情况
            console.log('wrong');
        }
      }
    };
    xhr.open('POST', '/manager/load_info', true);
    const fd = new FormData()
    fd.set('id', id)
    fd.set('type', "tour")
    xhr.send(fd)
}

function search_now(list, pattern) {
    const options = {
        threshold: 0.2,
        tokenize:true,
        keys: [
            "name"
        ]
    };

    if (pattern === '' || pattern == null){
        return list;
    }
    const fuse = new Fuse(list, options);
    let result = fuse.search(pattern);
    for (let i = 0; i < result.length; i++) {
        result[i] = result[i].item;
    }
    return  result;
}
