const item_container = document.getElementById("item-container")
const search_box = document.getElementById("search_box")

function search_customers() {
    let q = search_box.value
    load_customers(q)
}

function load_customers(pattern) {

    let xhr = new XMLHttpRequest()
    const fd = new FormData()
    xhr.open('POST', '/manager/load_customers', true)
    xhr.send(fd)

    // set animation after email send / error notification for registered email
    xhr.onload = function () {
        items = JSON.parse(xhr.responseText)['data']
        console.log(items)
        console.log(pattern)
        items = search_now(items, pattern)
        item_container.innerHTML = ''
        for (let i = 0; i < items.length; i++) {
            let tr = document.createElement("tr");
            tr.className = "table__row";
            s = `
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
                                        <td class="table__td">
                                            <div class="media-item media-item--medium">
                                                <a class="media-item__icon color-red">
                                                    <div class="media-item__icon-text">FB</div>
                                                    <img class="media-item__thumb" src="https://avatar.oxro.io/avatar.svg?name=${items[i].nickname}" alt="#">
                                                </a>
                                                <div class="media-item__right">
                                                    <h5 class="media-item__title">${items[i].nickname}</h5>
                                                </div>
                                            </div>
                                        </td>
                                        <td class="table__td text-light-theme">${items[i].email}
                                        </td>
                                        <td class="table__td text-dark-theme">${items[i].wallet}</td>
                                        <td class="table__td text-light-theme text-nowrap">${items[i].phone == null ? "not set" : items[i].phone}
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
                                                            <li class="dropdown-items__item"><a class="dropdown-items__link" href="/manager/customer_detail?id=${items[i].id}"><span class="dropdown-items__link-icon">
                                      <svg class="icon-icon-view">
                                        <use xlink:href="#icon-view"></use>
                                      </svg></span>Details</a>
                                                            </li>
                                                        </ul>
                                                    </div>
                                                </div>
                                            </div>
                                        </td>`
            tr.innerHTML = s
            item_container.appendChild(tr)
            let tr2 = document.createElement("tr");
            tr2.innerHTML = 'table__space'
            tr2.innerHTML = '<td colspan="6"></td>'
            item_container.appendChild(tr2)
        }
    }
}

load_customers()
console.log('loading customer')

function search_now(list, pattern) {
    const options = {
        threshold: 0.2,
        tokenize:true,
        keys: [
            "email",
            "id",
            "nickname",
            "phone",
        ]
    };

    if (pattern === ''){
        return list;
    }
    const fuse = new Fuse(list, options);
    let result = fuse.search(pattern);
    for (let i = 0; i < result.length; i++) {
        result[i] = result[i].item;
    }
    return  result;
}