var $messages = $(".messages-content"),
  customerName = "",
  customerId = -1,
  isLoggedIn = false,
  loginPageUrl = "",
  usingBot = true, // use bot by default
  botAvatarUrl = window.botAvatarUrl,
  socket = null,
  namespace = null,
  h,
  i = 0;

$(window).load(function () {
  initGlobalVars();
  $("#to-show-pic-upload").hide();
  $messages.mCustomScrollbar();
  setupListeners();
  doSend("Hello")
});

function initGlobalVars() {
  // get the customerName by post request to /get_session_customer_info
  $.ajax({
    type: "GET",
    url: "/get_session_customer_info",
    // data: {},
    timeout: 15000, // timeout after 15 seconds
    success: function (responseFromServer) {
      isLoggedIn = responseFromServer.isLoggedIn;
      if (isLoggedIn) {
        // loginPageUrl = "Not Needed Anymore"
        customerName = responseFromServer.nickname;
        customerId = responseFromServer.cusId;
      } else if (isLoggedIn == false) {
        customerName = "anon"; // fallback to anon
        customerId = -1;
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

function setupListeners() {
  // $(".history-loader").click(function () {
  //   socket.emit("req4history", { cusId: customerId });
  //   // then we remove the click2loadHistoryTxt
  //   $(".mCSB_container .history-loader").remove();
  // });

  $("#send-pic").on("change", function () {
    var formData = new FormData();
    var pic = $(this).get(0).files[0];
    formData.append("pic", pic);
    $.ajax({
      url: "/upload_pic",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (data) {
        if (data.code === 0) {
          hashed_filename = data.hashed_filename;
          console.log("Successfully uploaded file " + hashed_filename);
          // then we send the pic message
          socket.emit("pic_message", {
            sender: customerName,
            pic_filename: hashed_filename,
          });
        } else {
          console.log("Failed to upload file with error code " + data.code);
        }
        $("#send-pic").val("");
      },
    });
  });
}

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar("scrollTo", "bottom", {
    scrollInertia: 10,
    timeout: 0,
  });
}

function setDateNow() {
  var now = new Date();
  var hour = now.getHours().toString();
  var minute = now.getMinutes().toString();
  insertTimeStampForMsg(hour, minute);
}

function setDate(dateTimeStr) {
  var dateTimeObj = new Date(dateTimeStr);
  var hour = dateTimeObj.getHours().toString();
  var minute = dateTimeObj.getMinutes().toString();
  insertTimeStampForMsg(hour, minute);
}

function insertTimeStampForMsg(hour, minute) {
  $('<div class="timestamp">' + hour + ":" + minute + "</div>").appendTo(
    $(".message:last")
  );
}

function clearInputBox() {
  $(".message-input").val(null);
}

function insertMyMessage(myMessage) {
  $('<div class="message message-personal">' + myMessage + "</div>")
    .appendTo($(".mCSB_container"))
    .addClass("new");
  setDateNow();
  updateScrollbar();
  i++; // not sure what this is for
}

function insertMyMessageWithTime(myMessage, dateTimeStr) {
  $('<div class="message message-personal">' + myMessage + "</div>")
    .appendTo($(".mCSB_container"))
    .addClass("new");
  setDate(dateTimeStr);
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
  setDateNow();
  updateScrollbar();
  i++;
}

function insertRespMessageWithTime(txtToInsert, dateTimeStr) {
  $(
    '<div class="message new"><figure class="avatar"><img src="' +
      botAvatarUrl +
      '" /></figure>' +
      txtToInsert +
      "</div>"
  )
    .appendTo($(".mCSB_container"))
    .addClass("new");
  setDate(dateTimeStr);
  updateScrollbar();
  i++;
}

function insertSysBroadcast(txtToInsert) {
  $("<p>" + txtToInsert + "</p>")
    .appendTo($(".mCSB_container"))
    .addClass("new");
  setDateNow();
  updateScrollbar();
  i++;
}

function insertSysBroadcastWithTime(txtToInsert, dateTimeStr) {
  $("<p>" + txtToInsert + "</p>")
    .appendTo($(".mCSB_container"))
    .addClass("new");
  setDate(dateTimeStr);
  updateScrollbar();
  i++;
}

$(".message-submit").click(function () {
  customerMessage = $(".message-input").val();
  if ($.trim(customerMessage) == "") {
    return false; // do not send empty message
  }
  doSend(customerMessage);
  clearInputBox();
});

$(window).on("keydown", function (e) {
  if (e.which == 13) {
    customerMessage = $(".message-input").val();
    if ($.trim(customerMessage) == "") {
      return false; // do not send empty message
    }
    doSend(customerMessage);
    clearInputBox();
    return false; // to prevent the page from refreshing
  }
});

function requestForHistory() {
  socket.emit("req4history", { cusId: customerId });
  // then we remove the click2loadHistoryTxt
  $(".mCSB_container .history-loader").remove();
}

function doSend(customerMessage) {
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
      // a response was received
      // if the response starts with a "#" then it is a command we parse it using ajax to post to /parse_bot_cmd
      if (chatbotAnswer.startsWith("#")) {
        // then it is a command
        parseBotCmd(chatbotAnswer);
      } else {
        // just a text response
        $(".message.loading").remove();
        insertRespMessage(chatbotAnswer);
      }
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

function parseBotCmd(sharpCommandTxt) {
  $.ajax({
    type: "POST",
    url: "/parse_bot_cmd",
    data: {
      cmd: sharpCommandTxt,
    },
    timeout: 15000,
    success: function (cmdParserResp) {
      $(".message.loading").remove();
      execCallbackParsedCmd(cmdParserResp);
    },
  });
}

function execCallbackParsedCmd(parsedResp) {
  if (parsedResp.do == "SWITCH") {
    changeToRealPersonCustomerService();
  } else if (parsedResp.do == "REDIRECT") {
    insertRespMessage("redirecting you to: " + parsedResp.redirect_url);
    // redirect to the url using jquery's window.location.href
    window.location.href = parsedResp.redirect_url;
  } else if (parsedResp.do == "TEXT") {
    // just a text response
    insertRespMessage(parsedResp.to_show);
  }
}

function changeToRealPersonCustomerService() {
  $("#to-show-pic-upload").show();
  if (isLoggedIn == false) {
    window.location.href = loginPageUrl;
    return;
  }
  usingBot = false;
  insertRespMessage(
    "Please wait while we connect you to a real person customer service..."
  );

  // when this func is called we establish a websocket connection to the server

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
    var isHistory = res.isHistory;
    var resSender = res.sender;
    var resMsgTxt = res.text;
    // console.log("received message: '" + resMsgTxt + "' from " + resSender);
    if (resMsgTxt) {
      if (resSender == customerName) {
        // own message sent to server
        if (isHistory) {
          var sentTime = res.sentTime;
          insertMyMessageWithTime(resMsgTxt, sentTime);
        } else {
          insertMyMessage(resMsgTxt);
        }
      } else {
        if (isHistory) {
          var sentTime = res.sentTime;
          insertRespMessageWithTime(resMsgTxt, sentTime);
        } else {
          insertRespMessage(resMsgTxt);
        }
      }
    }
  });
}

function clickProfile() {
  toClick = document.getElementById("profile");
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
