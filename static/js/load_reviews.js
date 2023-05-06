let cur_category = 'all'
let cur_status = 'all'
let cur_pattern = ''
const item_container = document.getElementById("item-container")
const search_box = document.getElementById("search_box")
let BASE_URL = window.location.origin


function search_reviews() {
    let q = search_box.value
    load_reviews(null, null, q)
}

function load_reviews(category, status, pattern=null) {
    if (category == null) {
        category = cur_category
    }
    if (status == null) {
        status = cur_status
    }
    if (pattern == null) {
        pattern = cur_pattern
    }
    cur_category = category
    cur_status = status
    cur_pattern = pattern
    let xhr = new XMLHttpRequest()
    const fd = new FormData()
    fd.set('category', category)
    xhr.open('POST', '/manager/load_reviews', true)
    xhr.send(fd)

    // set animation after email send / error notification for registered email
    xhr.onload = function() {
        items = JSON.parse(xhr.responseText)['content']
        items = search_now(items, cur_pattern)
        item_container.innerHTML = ''
        for (let i = 0; i < items.length; i++) {
            let tr = document.createElement("tr");
            tr.className = "table__row";

            console.log(items[i].category)
            if (cur_category !== items[i].category && cur_category !== 'all') {
                continue;
            }

            if (cur_status !== items[i].rating.toString() && cur_status !== 'all') {
                continue
            }
            items[i].rating = "\u2B50".repeat(items[i].rating)
            if (items[i].content.length > 35) {
                items[i].content = items[i].content.substring(0, 34) + "..."
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
                                    <td class="table__td"><span class="text-light-theme">${items[i].reviewed_product.name}</span>
                                    </td>
                                    <td class="table__td text-dark-theme">${items[i].customer.email}</td>
                                    <td class="table__td text-overflow maxw-260"><span class="text-light-theme">${items[i].content}</span>
                                    </td>
                                    <td class="table__td">
                                        <div class="table__status"></span>${items[i].rating}</div>
                                    </td>
                                    <td class="table__td text-nowrap"><span class="text-light-theme">${items[i].date}</span>  
                                    </td>
                                    <td class="table__td">
                                        <div class="table__status"><span class="table__status-icon color-green"></span> Published</div>
                                    </td>
                                    <td class="table__td table__actions">
                                
                                    </td>
                                </tr>`
            tr.innerHTML = s
            item_container.appendChild(tr)
        }
    }
}

load_reviews(cur_category, 'all')

function clearInputs(){
    location.reload();
}

function search_now(list, pattern) {
    const options = {
        threshold: 0.2,
        tokenize:true,
        keys: [
            "customer.email"
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

