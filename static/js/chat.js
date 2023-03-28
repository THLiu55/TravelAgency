var $messages = $('.messages-content'),
  d, h, m,
  i = 0;

$(window).load(function () {
  $messages.mCustomScrollbar();
  setTimeout(function () {
    fakeMessage();
  }, 100);
});

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0
  });
}

function setDate() {
  d = new Date()
  if (m != d.getMinutes()) {
    m = d.getMinutes();
    $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
  }
}

function insertMessage() {
  msg = $('.message-input').val();
  if ($.trim(msg) == '') {
    return false;
  }
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  $('.message-input').val(null);
  updateScrollbar();
  // setTimeout(function () {
  //   fakeMessage();
  // }, 1000 + (Math.random() * 20) * 100);
  setTimeout(function () {
    realMessageFromBot(msg);
  }, 1000 + (Math.random() * 20) * 100);
}

$('.message-submit').click(function () {
  insertMessage();
});

$(window).on('keydown', function (e) {
  if (e.which == 13) {
    insertMessage();
    return false;
  }
})

var Fake = [
  'Hi there, I\'m Fabio and you?',
  'Nice to meet you',
  'How are you?',
  'Not too bad, thanks',
  'What do you do?',
  'That\'s awesome',
  'Codepen is a nice place to stay',
  'I think you\'re a nice person',
  'Why do you think that?',
  'Can you explain?',
  'Anyway I\'ve gotta go now',
  'It was a pleasure chat with you',
  'Time to make a new codepen',
  'Bye',
  ':)'
]

function fakeMessage() {
  if ($('.message-input').val() != '') {
    return false;
  }
  $('<div class="message loading new"><figure class="avatar"><img src="../static/image/robot.svg" /></figure><span></span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();

  setTimeout(function () {
    $('.message.loading').remove();
    $('<div class="message new"><figure class="avatar"><img src="../static/image/robot.svg" /></figure>' + Fake[i] + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    updateScrollbar();
    i++;
  }, 1000 + (Math.random() * 20) * 100);

}

function realMessageFromBot(yourMessage) {
  if ($('.message-input').val() != '') {
    return false;
  }
  $('<div class="message loading new"><figure class="avatar"><img src="../static/image/robot.svg" /></figure><span></span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();

  // get the chatbot response by post request to /get_chatbot_answer
  $.ajax({
    type: "POST",
    url: "/get_chatbot_answer",
    data: {
      'msg': yourMessage
    },
    success: function (data) {
      $('.message.loading').remove();
      $('<div class="message new"><figure class="avatar"><img src="../static/image/robot.svg" /></figure>' + data + '</div>').appendTo($('.mCSB_container')).addClass('new');
      setDate();
      updateScrollbar();
      i++;
    }
  })
}

// these are the functions for the cart unfold and fold
var fold = document.getElementById('btnfold')
var note = document.getElementById('notebook')
var unfold = document.getElementById('shopincart')
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
      document.getElementById('shopincart').style.display = 'block';
      // set the whole cart to display none
      document.getElementById('notebook').style.display = 'none';
      clearInterval(timer);
    }
    note.style.height = h + 'px';
  }, 10);
}
var note = document.getElementById('notebook')
var unfold = document.getElementById('shopincart')
var timer = null,
  timer2 = null,
  noteHeight = note.clientHeight;
// if the user click the unfold button, the cart will unfold
unfold.onclick = function () {
  document.getElementById('notebook').classList.remove('listneg');

  var h = 0;
  clearInterval(timer2);
  timer2 = setInterval(function () {
    // set the speed of unfolding
    h += 10;
    if (h >= noteHeight) {
      h = noteHeight;
      // set the unfold button to display none
      document.getElementById('shopincart').style.display = 'block';
      clearInterval(timer2);
    }
    note.style.height = h + 'px';
  }, 10);


  document.getElementById('notebook').style.display = 'flex';
}