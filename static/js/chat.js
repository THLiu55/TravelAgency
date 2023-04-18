var $messages = $(".messages-content"),
  customerName = "",
  isLoggedIn = false,
  loginPageUrl = "",
  usingBot = true, // use bot by default
  botAvatarUrl = window.botAvatarUrl,
  socket = null,
  namespace = null,
  d,
  h,
  m,
  i = 0;

$(window).load(function () {
  initGlobalVars();
  $messages.mCustomScrollbar();
  setTimeout(function () {
    botMessage =
      "Hello, " +
      customerName +
      "! I am a chatbot. I can help you with your order. If you want to talk to a real person, please type 'change to real person customer service' in the chatbox below. Thank you!";
    insertRespMessage(botMessage);
  }, 100);
});

function initGlobalVars() {
  // get the customerName by post request to /get_session_customer_name
  $.ajax({
    type: "POST",
    url: "/get_session_customer_name",
    data: {},
    timeout: 15000, // timeout after 15 seconds
    success: function (responseFromServer) {
      isLoggedIn = responseFromServer.isLoggedIn;
      if (isLoggedIn) {
        // loginPageUrl = "Not Needed Anymore"
        customerName = responseFromServer.nickname;
      } else if (isLoggedIn == false) {
        customerName = "anon"; // fallback to anon
        loginPageUrl = responseFromServer.loginPageUrl;
      }
    },
    error: function (xhr, status, error) {
      // an error occurred
      console.log("ERROR_" + status + "_" + error.message);
      customerName = "anon"; // fallback to anon
    },
  });

  // currently we set namespace to /chat
  namespace = "/chat";
}

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar("scrollTo", "bottom", {
    scrollInertia: 10,
    timeout: 0,
  });
}

function setDate() {
  d = new Date();
  if (m != d.getMinutes()) {
    m = d.getMinutes();
    $('<div class="timestamp">' + d.getHours() + ":" + m + "</div>").appendTo(
      $(".message:last")
    );
  }
}

function clearInputBox() {
  $(".message-input").val(null);
}

function insertMyMessage(myMessage) {
  $('<div class="message message-personal">' + myMessage + "</div>")
    .appendTo($(".mCSB_container"))
    .addClass("new");
  setDate();
  updateScrollbar();
  i++; // not sure what this is for
}

function insertRespMessage(txtToInsert) {
  $(
    '<div class="message new"><figure class="avatar"><img src="' +
      botAvatarUrl +
      '" /></figure>' +
      txtToInsert +
      "</div>"
  )
    .appendTo($(".mCSB_container"))
    .addClass("new");
  setDate();
  updateScrollbar();
  i++;
}

$(".message-submit").click(function () {
  doSend();
  clearInputBox();
});

$(window).on("keydown", function (e) {
  if (e.which == 13) {
    doSend();
    clearInputBox();
    return false; // to prevent the page from refreshing
  }
});

function doSend() {
  customerMessage = $(".message-input").val();

  if (customerMessage == "change to real person customer service") {
    // currently there are only one keyword to change to real person customer service
    clearInputBox();
    insertMyMessage(customerMessage);
    customerMessage = "";
    changeToRealPersonCustomerService();
  }

  if ($.trim(customerMessage) == "") {
    return false; // do not send empty message
  }

  if (usingBot) {
    insertMyMessage(customerMessage); // need not to check if the message is sent to server successfully
    getAndInsertRespMessageFromBot(customerMessage);
  } else {
    // need not to insert message manually, because the server will send back the message to the client
    var text = customerMessage;
    var sender = customerName;
    socket.emit("message", { sender: sender, text: text });
  }
}

function getAndInsertRespMessageFromBot(yourMessage) {
  $(
    '<div class="message loading new"><figure class="avatar"><img src="' +
      botAvatarUrl +
      '" /></figure><span></span></div>'
  ).appendTo($(".mCSB_container"));
  updateScrollbar();

  // get the chatbot response by post request to /get_chatbot_answer
  $.ajax({
    type: "POST",
    url: "/get_chatbot_answer",
    data: {
      msg: yourMessage,
    },
    timeout: 15000, // timeout after 15 seconds
    success: function (chatbotAnswer) {
      $(".message.loading").remove();
      insertRespMessage(chatbotAnswer);
    },
    error: function (xhr, status, error) {
      // an error occurred
      $(".message.loading").remove();
      console.log("ERROR_" + status + "_" + error.message);
      insertRespMessage(
        "Sorry, I am having some problems. Please try again later."
      );
    },
  });
}

function changeToRealPersonCustomerService() {
  if (isLoggedIn == false) {
    window.location.href = loginPageUrl;
    return;
  }
  usingBot = false;
  insertRespMessage(
    "Please wait while we connect you to a real person customer service..."
  );

  // when this func is called we establish a websocket connection to the server

  // namespace = '/socketest'; // now it is initialized in initGlobalVars()
  socket = io.connect(
    location.protocol +
      "//" +
      document.domain +
      ":" +
      location.port +
      namespace,
    { autoJoin: false }
  );

  // set client side event handler
  socket.on("message", function (res) {
    var resSender = res.sender;
    var resMsgTxt = res.text;
    console.log("received message: '" + resMsgTxt + "' from " + resSender);
    if (resMsgTxt) {
      if (resSender == customerName) {
        // own message sent to server
        insertMyMessage(resMsgTxt);
      } else {
        insertRespMessage(resMsgTxt);
      }
    }
  });
}

/* FRONT END JS */

// these are the functions for the cart unfold and fold
var fold = document.getElementById("btnfold");
var note = document.getElementById("notebook");
var unfold = document.getElementById("shopincart");
var timer = null,
  timer2 = null,
  noteHeight = note.clientHeight;
// when user click the button, the cart will fold
fold.onclick = function () {
  // get the height of the note cart
  var h = noteHeight;
  clearInterval(timer);
  timer = setInterval(function () {
    // set the speed of folding
    h -= 10;
    if (h <= 0) {
      h = 0;
      // set the unfold button to display
      document.getElementById("shopincart").style.display = "block";
      // set the whole cart to display none
      document.getElementById("notebook").style.display = "none";
      clearInterval(timer);
    }
    note.style.height = h + "px";
  }, 10);
};
var note = document.getElementById("notebook");
var unfold = document.getElementById("shopincart");
var timer = null,
  timer2 = null,
  noteHeight = note.clientHeight;
// if the user click the unfold button, the cart will unfold
unfold.onclick = function () {
  document.getElementById("notebook").classList.remove("listneg");

  var h = 0;
  clearInterval(timer2);
  timer2 = setInterval(function () {
    // set the speed of unfolding
    h += 10;
    if (h >= noteHeight) {
      h = noteHeight;
      // set the unfold button to display none
      document.getElementById("shopincart").style.display = "block";
      clearInterval(timer2);
    }
    note.style.height = h + "px";
  }, 10);

  document.getElementById("notebook").style.display = "flex";
};

/* END FRONTEND JS */
