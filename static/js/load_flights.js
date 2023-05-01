let cur_status = "All Status"
let cur_category = "All Category"
const item_container = document.getElementById("item-container")
const modifyProduct = document.getElementById("modifyProduct")
let BASE_URL = window.location.origin

function load_flights(published, category) {
    if (published == null) {
        published = cur_status
    }
    if (category == null) {
        category = cur_category
    }
    cur_category = category
    cur_status = published
    let xhr = new XMLHttpRequest()
    const fd = new FormData()
    fd.set('publish', published)
    fd.set('category', category)
    xhr.open('POST', '/manager/load_flights', true)
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
                                <td class="table__td">${items[i].departure}</td>
                                <td class="table__td"><span class="text-grey">${items[i].destination}</span>
                                </td>
                                <td class="table__td"><span>${items[i].take_off_time}</span>
                                </td>
                                <td class="d-none d-lg-table-cell table__td"><span
                                        class="text-grey">${items[i].landing_time}</span>
                                </td>
                                <td class="d-none d-sm-table-cell table__td">
                                    ${status_img}
                                </td>
                                <td class="table__td table__actions">
                                        <div class="items-more">
                                            <button class="items-more__button" style="max-width: 100px;max-height: 30px; margin-left: 0px; padding-left: 0px;margin-right: 0px; padding-right: 0px;">
                                                <svg class="icon-icon-more">
                                                    <use xlink:href="#icon-more"></use>
                                                </svg>
                                            </button>
                                            <div class="dropdown-items dropdown-items--right">
                                                <div class="dropdown-items__container">
                                                    <ul class="dropdown-items__list">
                                                        <li class="dropdown-items__item">
                                                        <a class="dropdown-items__link">
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

load_flights(cur_status, cur_category)

function delete_item(id) {
    let xhr = new XMLHttpRequest()
    const fd = new FormData()
    fd.set('id', id)
    console.log(id)
    xhr.open('POST', '/manager/delete_flight', true)
    xhr.send(fd)

    // set animation after email send / error notification for registered email
    xhr.onload = function() {
        load_flights(cur_status, cur_category)
    }
}

function clearInputs() {
    // const inputs = document.getElementsByTagName('input');
    // const textareas = document.getElementsByTagName('textarea');
    // const selects = document.getElementsByTagName('select');
    // const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    // for (let i = 0; i < inputs.length; i++) {
    //     inputs[i].value = '';
    // }
    // for (let i = 0; i < textareas.length; i++) {
    //     textareas[i].value = '';
    // }
    // for (let i = 0; i < selects.length; i++) {
    //     selects[i].selectedIndex = 0;
    // }
    // for (let i = 0; i < checkboxes.length; i++) {
    //     checkboxes[i].checked = false;
    // }

    location.reload();
}