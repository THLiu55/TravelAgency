let cur_category = 'all'
let cur_status = 'all'
let cur_key = ''
let cur_sort_by = 0
let cur_page = 0
const item_container = document.getElementById("item-container")
const deleteProduct = document.getElementById("deleteProduct")
const page_num_text = document.getElementById("cur_page_num")
let BASE_URL = window.location.origin


function query() {
    let search_box = document.getElementById("search_box")
    let q = search_box.value
    load_orders(null, null, q)
}

function load_orders(category, status, key=null, sort_by=null, page=0) {
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
    cur_page = page
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
        tmp = []
        for (let i = 0; i < items.length; i++) {
            if (cur_category !== items[i].category && cur_category !== 'all') {
                continue;
            }
            if (cur_key !== items[i].productID.toString() && cur_key !== '') {
                continue;
            }
            tmp.push(items[i])
        }
        tmp = convertTo2DList(tmp)
        if (cur_page >= tmp.length) {
            cur_page = tmp.length - 1;
        }
        items = tmp[cur_page]
        page_num_text.innerHTML = `${cur_page + 1}/${tmp.length}`
        for (let i = 0; i < items.length; i++) {
            let tr = document.createElement("tr");
            tr.className = "table__row";

            if (items[i].isDeleted) {
                status_s = `<div className="table__status"><span class="marker-item color-red"></span> Deleted </div>`
            } else {
                status_s = `<div className="table__status"><span class="marker-item color-green"></span> Active </div>`
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
                                                    <li class="dropdown-items__item" >
                                                        <a class="dropdown-items__link" >
<!--                                                        onclick="delete_order(${items[i].id})"-->
                                                        <span class="dropdown-items__link-icon" style="padding-left: 50%;">
                                                            <button id="orderDelete" onclick="DeleteSpan(${items[i].id}, '${items[i].category}')" data-toggle="modal"  data-target="#deleteOrder" data-modal="#button_Delete" style="max-width: 100px;max-height: 30px;  white-space: nowrap;">
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

        const button_Delete = document.querySelectorAll("#button_Delete")
        button_Delete.forEach(item => {
            item.addEventListener('click', () => {
                deleteProduct.classList.add("is-active", "is-animate")
            })
        })
    }
}

load_orders(cur_category, 'all')

function clearInputs(){
    location.reload();
}

function delete_order(id, type, reason) {
    let xhr = new XMLHttpRequest()
    const fd = new FormData()
    fd.set('id', id)
    fd.set('type', type)
    console.log(reason)
    fd.set('reason', reason)
    xhr.open('POST', '/manager/delete_order', true)
    xhr.send(fd)

    // set animation after email send / error notification for registered email
    xhr.onload = function() {
        location.reload();
    }
}

// 当用户点击按钮时打开模态框
function DeleteSpan (id, type) {
    var modal = document.getElementById("DeleteModal");
    modal.style.display = "block";
    var confirm_btn = document.getElementById("confirmButton")
    confirm_btn.onclick = function() {
        var inputText = document.getElementById('reason_delete').value;
        delete_order(id, type, inputText)
        modal.style.display = "none";
    }
}

function CancelDelete () {
    var modal = document.getElementById("DeleteModal");
    modal.style.display = "none";
}


function convertTo2DList(inputList) {
  var outputList = [];
  var sublist = [];

  for (var i = 0; i < inputList.length; i++) {
    sublist.push(inputList[i]);

    if (sublist.length === 7) {
      outputList.push(sublist);
      sublist = [];
    }
  }

  // If there are any remaining elements in the sublist, add them to the output list
  if (sublist.length > 0) {
    outputList.push(sublist);
  }

  return outputList;
}

function prev_page() {
    load_orders(null, null, null, null, Math.max(cur_page - 1, 0))
}

function next_page() {
    load_orders(null, null, null, null, cur_page + 1)
}