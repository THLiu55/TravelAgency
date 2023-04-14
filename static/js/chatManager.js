// global vars
var theDivToInsertMessages;
var currentSelectedCustomerName = "";
var currentSelectedCustomerId = "";

$(document).ready(function () {
  initGlobalVars();
  activateUserListItem();
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
      target_customer_id: currentSelectedCustomerId,
    });
  });
  socket.on("message", function (res) {
    var sender = res.sender;
    var t = res.text;
    console.log("received message: " + t + ", from: " + sender);
    if (sender == currentSelectedCustomerName) {
      insertRespMessageNow(sender, t);
      // TODO: scroll to bottom of chat
    } else if (sender == "TestAdminUser") {
      insertMyMessageNow(t);
    } else {
      console.log("Another customer ( " + sender + " )'s message: " + t);
    }
  });
  $("#send-message").click(function () {
    var text = $(".chat-details__input").val();
    $(".chat-details__input").val("");
    socket.emit("message", {
      // sender: $("#sender").text(),
      sender: "TestAdminUser", // TODO: 2b Dynamic
      text: text,
      target_customer_id: currentSelectedCustomerId,
    });
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
  currentSelectedCustomerName =
    document.querySelector("#customer-nickname").innerText;
  currentSelectedCustomerId = document.querySelector("#customer-id").innerText;
}

function updateCurrentSelection(customerName) {
  currentSelectedCustomerName = customerName;
}

function activateUserListItem() {
  var correctId = "activatee-" + currentSelectedCustomerName
  var targetLocation = document.getElementById(correctId)
  targetLocation.classList.add("active");
}

function insertRespMessageNow(senderName, respMsgTxt) {
  const now = new Date();
  insertRespMessage(senderName, respMsgTxt, now);
}

function insertRespMessage(senderName, respMsgTxt, deliveredTime) {
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
      deliveredTime.getHours() +
      ":" +
      deliveredTime.getMinutes() +
      '</div><div class="chat-message__files"></div></div></div>'
  );
  RespMessageElemToAppend.appendTo(theDivToInsertMessages);
}

function insertMyMessageNow(myMsgTxt) {
  const now = new Date();
  insertMyMessage(myMsgTxt, now);
}

function insertMyMessage(myMsgTxt, sentTime) {
  const myMessageElemToAppend = $(
    '<div class="chat-message chat-message--answer"><div class="chat-message__content"><a class="chat-message__icon color-red" href="#"><div class="chat-message__icon-text">' +
      "T" +
      '</div><img src="https://avatar.oxro.io/avatar.svg?name=' +
      "TestAdminUser" +
      '" alt="#" /></a><div class="chat-message__right"><div class="chat-message__messages"><div class="chat-message__message-group"><div class="chat-message__message-item"><p class="chat-message__item-text">' +
      myMsgTxt +
      ' </p></div><div class="chat-message__tools active"><div class="items-more"><button class="items-more__button"><svg class="icon-icon-more"><use xlink:href="#icon-more"></use></svg></button></div><div class="chat-message__tools-item"><button class="button-icon button-icon--grey"><span class="button-icon__icon"><svg class="icon-icon-drafts"><use xlink:href="#icon-drafts"></use></svg></span></button></div><div class="chat-message__tools-item"><button class="button-icon button-icon--grey"><span class="button-icon__icon"><svg class="icon-icon-trash"><use xlink:href="#icon-trash"></use></svg></span></button></div></div></div></div></div></div><div class="chat-message__bottom"><div class="chat-message__time">' +
      sentTime.getHours() +
      ":" +
      sentTime.getMinutes() +
      '</div><div class="chat-message__files"></div></div></div>'
  );
  myMessageElemToAppend.appendTo(theDivToInsertMessages);
}
