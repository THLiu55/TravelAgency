// global vars
var theDivToInsertMessages;
var selectedCustomerUserListItem;
var selectedCustomerName = "";
var selectedCustomerId = "";
var adminUserName = "";

$(document).ready(function () {
  try {
    initGlobalVars();
  } catch (error) {
    if (error.message == "AllClearException") {
      console.log("all clear, good to go");
      return;
    }
  }
  // activateUserListItem();
  activateCurrentUserDetailView();
  namespace = "/chat";
  const socket = io.connect(
    location.protocol +
      "//" +
      document.domain +
      ":" +
      location.port +
      namespace,
    { autoJoin: false }
  );
  socket.on("connect", function () {
    socket.emit("join", {
      target_customer_id: selectedCustomerId,
    });
    console.log("joinning room: " + selectedCustomerId);
    socket.emit("read", {
      cusId: selectedCustomerId,
    });
  });
  socket.on("message", function (res) {
    var isHistory = res.isHistory;
    var sender = res.sender;
    var t = res.text;
    console.log("received message: " + t + ", from: " + sender);
    if (isHistory == false || isHistory == undefined) {
      // i know, stupid
      // history loading is only for customer
      if (sender == selectedCustomerName) {
        insertRespMessageNow(sender, t);
        // TODO: scroll to bottom of chat
      } else if (sender == adminUserName) {
        insertMyMessageNow(t);
      } else if (sender == "system") {
        console.log("system message received: " + t);
      } else {
        updateUnreadCounter(sender);
        updateUnreadMsgPreview(sender, t);
      }
    }
  });
  $("#send-message").click(function () {
    var text = $(".chat-details__input").val();
    $(".chat-details__input").val("");
    socket.emit("message", {
      sender: adminUserName,
      text: text,
      target_customer_id: selectedCustomerId,
    });
  });
  $("#chat-inputbox").keypress(function (e) {
    if (e.which == 13) {
      var text = $(".chat-details__input").val();
      $(".chat-details__input").val("");
      socket.emit("message", {
        sender: adminUserName,
        text: text,
        target_customer_id: selectedCustomerId,
      });
    }
  });
  $(".chat-users__list-item").click(function () {
    if ($(this).find(".chat-users__item").hasClass("active")) {
      return;
    }
    socket.emit("leave", {
      target_customer_id: selectedCustomerId, // leave the previous room
    });
    updateCusSelection($(this));
    socket.emit("join", {
      target_customer_id: selectedCustomerId, // join the new room
    });
    socket.emit("read", {
      cusId: selectedCustomerId,
    });
    clearUnreadCounterInItem($(this));
  });
});

function initGlobalVars() {
  const potentialTargetDivs = document.querySelectorAll(".simplebar-content");
  var correctIdx = 0;
  for (let i = 0; i < potentialTargetDivs.length; i++) {
    if (
      potentialTargetDivs[i].parentElement.parentElement.parentElement
        .parentElement.parentElement ==
      document.querySelector(".chat-details__content")
    ) {
      correctIdx = i;
    } // seems like i = 5 is the correct index
  }
  theDivToInsertMessages = potentialTargetDivs[correctIdx];

  adminUserName = document.querySelector("#admin-username-txt").innerText;
  firstCusListItem = $("#unread-customers-list").find("li:first"); // default to the first customer
  if (firstCusListItem.length == 0) {
    throw new Error("AllClearException");
  }
  updateCusSelection(firstCusListItem);
  manuallyActivateItem(firstCusListItem);
  clearUnreadCounterInItem(firstCusListItem);
}

function updateCusSelection(clickedLoc) {
  selectedCustomerUserListItem = clickedLoc;
  selectedCustomerName = clickedLoc.find(".customer-nickname-h5").text();
  selectedCustomerId = clickedLoc.find(".customer-id-h5").text();
  $("#selected-customer-avatar").attr(
    "src",
    clickedLoc.find(".customer-avatar").attr("src")
  );
  $("#selected-customer-nickname").text(selectedCustomerName);
  $("#selected-customer-id").text(selectedCustomerId);

  // load the history of the selected customer
  // using ajax to get from /staff_load_chat_history/<customer_id>
  theDivToInsertMessages.innerHTML = "";
  $.ajax({
    type: "GET",
    url: "/staff_load_chat_history/" + selectedCustomerId,
    success: function (data) {
      console.log("success");
      console.log(data);
      for (let i = 0; i < data.length; i++) {
        const msg = data[i];
        if (msg.isByCustomer == true) {
          insertRespMessage(
            selectedCustomerName,
            msg.content,
            new Date(msg.sentTime)
          );
        } else if (msg.isByCustomer == false) {
          insertMyMessage(msg.content, new Date(msg.sentTime));
        } else {
          console.log("error: isByCustomer is not defined");
        }
      }
    },
    error: function (data) {
      console.log("error");
      console.log(data);
    },
  });
}

function clearUnreadCounterInItem(targetItem) {
  targetCounter = targetItem.find(".unread-counter");
  targetCounter.text("0");
  targetCounter.style.display = "none";
}

function updateUnreadCounter(senderName) {
  var correctId = "unread-counter-" + senderName;
  var targetLocation = document.getElementById(correctId);
  console.log(targetLocation + " is the target location for sender: " + senderName);
  var currentCount = parseInt(targetLocation.innerText);
  targetLocation.innerText = currentCount + 1;
  targetLocation.style.removeProperty("display");
}

function updateUnreadMsgPreview(senderName, msg) {
  var correctId = "last-msg-preview-" + senderName;
  var targetLocation = document.getElementById(correctId);
  targetLocation.innerText = msg;
}

function manuallyActivateItem(theItem) {
  var correctId = "activatee-" + selectedCustomerName;
  var targetLocation = theItem.find("#" + correctId)[0];
  targetLocation.classList.add("active");
}

function activateCurrentUserDetailView() {
  $("#selected-customer-nickname").text(selectedCustomerName);
  $("#selected-customer-id").text(selectedCustomerId);
}

function insertRespMessageNow(senderName, respMsgTxt) {
  const now = new Date();
  insertRespMessage(senderName, respMsgTxt, now);
}

function insertRespMessage(senderName, respMsgTxt, deliveredTimeObj) {
  const RespMessageElemToAppend = $(
    '<div class="chat-message"><div class="chat-message__content"><a class="chat-message__icon color-teal" href="#"><div class="chat-message__icon-text">' +
      senderName[0] +
      '</div><img src="https://avatar.oxro.io/avatar.svg?name=' +
      senderName +
      '" alt="' +
      senderName +
      '"></a><div class="chat-message__right"><div class="chat-message__messages"><div class="chat-message__message-group"><div class="chat-message__message-item"><p class="chat-message__item-text">' +
      respMsgTxt +
      '</p></div></div></div></div></div><div class="chat-message__bottom"><div class="chat-message__time">' +
      deliveredTimeObj.getHours() +
      ":" +
      deliveredTimeObj.getMinutes() +
      '</div><div class="chat-message__files"></div></div></div>'
  );
  RespMessageElemToAppend.appendTo(theDivToInsertMessages);
}

function insertMyMessageNow(myMsgTxt) {
  const now = new Date();
  insertMyMessage(myMsgTxt, now);
}

function insertMyMessage(myMsgTxt, sentTimeObj) {
  const myMessageElemToAppend = $(
    '<div class="chat-message chat-message--answer"><div class="chat-message__content"><a class="chat-message__icon color-red" href="#"><div class="chat-message__icon-text">' +
      "T" +
      '</div><img src="https://avatar.oxro.io/avatar.svg?name=' +
      adminUserName +
      '" alt="#" /></a><div class="chat-message__right"><div class="chat-message__messages"><div class="chat-message__message-group"><div class="chat-message__message-item"><p class="chat-message__item-text">' +
      myMsgTxt +
      ' </p></div><div class="chat-message__tools active"><div class="items-more"><button class="items-more__button"><svg class="icon-icon-more"><use xlink:href="#icon-more"></use></svg></button></div><div class="chat-message__tools-item"><button class="button-icon button-icon--grey"><span class="button-icon__icon"><svg class="icon-icon-drafts"><use xlink:href="#icon-drafts"></use></svg></span></button></div><div class="chat-message__tools-item"><button class="button-icon button-icon--grey"><span class="button-icon__icon"><svg class="icon-icon-trash"><use xlink:href="#icon-trash"></use></svg></span></button></div></div></div></div></div></div><div class="chat-message__bottom"><div class="chat-message__time">' +
      sentTimeObj.getHours() +
      ":" +
      sentTimeObj.getMinutes() +
      '</div><div class="chat-message__files"></div></div></div>'
  );
  myMessageElemToAppend.appendTo(theDivToInsertMessages);
}
