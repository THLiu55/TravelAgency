var messageReceivedHtmlTemplateBefore = '<div class="chat-message"><div class="chat-message__content"><a class="chat-message__icon color-teal" href="#"><div class="chat-message__icon-text">DP</div><img src="../static/img/content/humans/item-5.jpg" alt="#" /></a><div class="chat-message__right"><div class="chat-message__messages"><div class="chat-message__message-group"><div class="chat-message__message-item"><p class="chat-message__item-text">'
var messageReceivedHtmlTemplateAfter = '<img src="../static/img/content/emoji-happy.svg" alt="#" /></p></div></div></div></div></div><div class="chat-message__bottom"><div class="chat-message__time">1 min ago</div><div class="chat-message__files"></div></div></div>'

var messageSentHtmlTemplateBefore = ''

var yourMessage = "TESTINGTESTING123"
function receiveMessage() {
    // if ($('.message-input').val() != '') {
    //     return false;
    // }
    console.log("receiveMessage() called")
    // setTimeout(function () {
        // $('.message.loading').remove();
        $(messageReceivedHtmlTemplateBefore + yourMessage + messageReceivedHtmlTemplateAfter).appendTo($('.chat-details__content'));
    // }, 1000 + (Math.random() * 20) * 100);

}