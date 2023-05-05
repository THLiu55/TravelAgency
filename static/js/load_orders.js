let cur_category = 'all'
let cur_status = 'all'
let cur_key = ''
let cur_sort_by = 0
const item_container = document.getElementById("item-container")
let BASE_URL = window.location.origin

function checkTimeStatus(start, end) {
  const now = new Date(); // get current date and time

  const startTime = new Date(start);
  const endTime = new Date(end);

  if (now < startTime) {
    return "waiting"; // the current time is before the start time
  } else if (now >= startTime && now <= endTime) {
    return "processing"; // the current time is between the start and end times
  } else {
    return "done"; // the current time is after the end time
  }
}

function query() {
    let search_box = document.getElementById("search_box")
    let q = search_box.value
    load_orders(null, null, q)
}

function load_orders(category, status, key=null, sort_by=null) {
    console.log('here')
    if (category == null) {
        category = cur_category
    }
    if (status == null) {
        status = cur_status
    }
    if (key === null) {
        key = cur_key
    }
    if (sort_by === null) {
        sort_by = cur_sort_by
    }
    cur_category = category
    cur_status = status
    cur_key = key
    cur_sort_by = sort_by
    let xhr = new XMLHttpRequest()
    const fd = new FormData()
    fd.set('category', category)
    xhr.open('POST', '/manager/load_orders', true)
    xhr.send(fd)

    // set animation after email send / error notification for registered email
    xhr.onload = function() {
        items = JSON.parse(xhr.responseText)['content']
        item_container.innerHTML = ''
        console.log(items[0])
        if (cur_sort_by === 0) {
            items.sort((a, b) => { if (a.end_time < b.end_time) return -1; if (a.end_time > b.end_time) return 1; return 0;});
        } else {
            items.sort((a, b) => a.cost - b.cost).reverse();
        }
        for (let i = 0; i < items.length; i++) {
            let tr = document.createElement("tr");
            tr.className = "table__row";
            order_status = checkTimeStatus(items[i].start_time, items[i].end_time)


            if (cur_status !== order_status && cur_status !== 'all') {
                continue;
            }

            if (cur_category !== items[i].category && cur_category !== 'all') {
                continue;
            }

            if (cur_key !== items[i].productID.toString() && cur_key !== '') {
                continue;
            }

            if (order_status === 'waiting') {
                status_s = `<div className="table__status"><span class="marker-item color-blue"></span></span> Waiting</div>`
            } else if (order_status === 'processing') {
                status_s = `<div className="table__status"><span class="marker-item color-orange"></span> Processing</div>`
            } else {
                status_s = `<div className="table__status"><span class="marker-item color-green"></span> Complete</div>`
            }

            if (items[i].isDeleted) {
                status_s = `<div className="table__status"><span class="marker-item color-red"></span> Deleted </div>`
            }

            s = `<tr class="table__row">
                                    <td class="table__td">
                                        <div class="table__checkbox table__checkbox--all">
                                            <label class="checkbox">
                                                <input type="checkbox" data-checkbox="product"><span class="checkbox__marker"><span class="checkbox__marker-icon">
                              <svg class="icon-icon-checked">
                                <use xlink:href="#icon-checked"></use>
                              </svg></span></span>
                                            </label>
                                        </div>
                                    </td>
                                    <td class="d-none d-lg-table-cell table__td"><span class="text-grey">${items[i].customer.nickname}</span>
                                    </td>
                                    <td class="table__td">${items[i].category}</td>
                                    <td class="d-none d-sm-table-cell table__td"><span class="text-grey">$ ${items[i].cost}</span>
                                    </td>
                                    <td class="table__td"><span>${items[i].start_time}</span>
                                    </td>
                                    <td class="table__td text-nowrap"><span class="text-grey">${items[i].end_time}</td>
                                    <td class="d-none d-sm-table-cell table__td">
                                        ${status_s}
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
                                                        <li class="dropdown-items__item"><a class="dropdown-items__link" href="/manager/invoice?id=${items[i].id}&type=${items[i].category}"><span class="dropdown-items__link-icon">
                                    <svg class="icon-icon-view">
                                      <use xlink:href="#icon-view"></use>
                                    </svg></span>Details</a>
                                                        </li>                                                     
                                                        <li class="dropdown-items__item"><a class="dropdown-items__link" onclick="delete_order(${items[i].id}, '${items[i].category}')"><span class="dropdown-items__link-icon">
                                    <svg class="icon-icon-trash">
                                      <use xlink:href="#icon-trash"></use>
                                    </svg></span>Delete</a>
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
    }
}

load_orders(cur_category, 'all')

function clearInputs(){
    location.reload();
}

function delete_order(id, type) {
    console.log('deleting')
    let xhr = new XMLHttpRequest()
    const fd = new FormData()
    fd.set('id', id)
    fd.set('type', type)
    xhr.open('POST', '/manager/delete_order', true)
    xhr.send(fd)

    // set animation after email send / error notification for registered email
    xhr.onload = function() {
        location.reload();
    }
}