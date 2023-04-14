let cur_category = 'all'
let cur_status = 'all'
const item_container = document.getElementById("item-container")
let BASE_URL = window.location.origin


function load_reviews(category, status) {
    if (category == null) {
        category = cur_category
    }
    if (status == null) {
        status = cur_status
    }
    cur_category = category
    cur_status = status
    let xhr = new XMLHttpRequest()
    const fd = new FormData()
    fd.set('category', category)
    xhr.open('POST', '/manager/load_reviews', true)
    xhr.send(fd)

    // set animation after email send / error notification for registered email
    xhr.onload = function() {
        items = JSON.parse(xhr.responseText)['content']
        item_container.innerHTML = ''
        for (let i = 0; i < items.length; i++) {
            let tr = document.createElement("tr");
            tr.className = "table__row";

            console.log(items[i].category)
            if (cur_category !== items[i].category && cur_category !== 'all') {
                continue;
            }

            console.log(items[i].rating)
            console.log(cur_status)
            console.log(' -------------- ')
            if (cur_status !== items[i].rating.toString() && cur_status !== 'all') {
                continue
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
                                    <td class="table__td text-dark-theme">${items[i].customer.nickname}</td>
                                    <td class="table__td text-overflow maxw-260"><span class="text-light-theme">${items[i].content}</span>
                                    </td>
                                    <td class="table__td">
                                        <div class="rating js-rating-stars" data-rating="${items[i].rating}" data-readonly="true"></div>
                                    </td>
                                    <td class="table__td text-nowrap"><span class="text-light-theme">${items[i].date}</span>  <span class="text-dark-theme">10:00</span>
                                    </td>
                                    <td class="table__td">
                                        <div class="table__status"><span class="table__status-icon color-green"></span> Published</div>
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
                                                        <li class="dropdown-items__item"><a class="dropdown-items__link"><span class="dropdown-items__link-icon">
                                    <svg class="icon-icon-view">
                                      <use xlink:href="#icon-view"></use>
                                    </svg></span>Details</a>
                                                        </li>
                                                        <li class="dropdown-items__item"><a class="dropdown-items__link"><span class="dropdown-items__link-icon">
                                    <svg class="icon-icon-duplicate">
                                      <use xlink:href="#icon-duplicate"></use>
                                    </svg></span>Duplicate</a>
                                                        </li>
                                                        <li class="dropdown-items__item"><a class="dropdown-items__link"><span class="dropdown-items__link-icon">
                                    <svg class="icon-icon-archive">
                                      <use xlink:href="#icon-archive"></use>
                                    </svg></span>Archive</a>
                                                        </li>
                                                        <li class="dropdown-items__item"><a class="dropdown-items__link"><span class="dropdown-items__link-icon">
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

load_reviews(cur_category, 'all')



