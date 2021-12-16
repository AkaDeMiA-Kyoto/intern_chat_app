'use strict';
const room_id = JSON.parse(document.getElementById('friend').textContent);
const user_id = JSON.parse(document.getElementById('user').textContent);
const friend_id = JSON.parse(document.getElementById('friend').textContent);
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + room_id
    + '/'
);



// ソケット受信時トークルームにチャットコンテナを追加
chatSocket.onmessage = function(e){

    const data = JSON.parse(e.data);

    let chatboard__content = document.createElement('li');
    let usericon = document.createElement('img');
    let name = document.createElement('p');
    let message = document.createElement('p');
    let time = document.createElement('p');

    chatboard__content.classList.add('chatboard__content');
    usericon.classList.add('friend__usericon');
    name.classList.add('chatboard__name');
    message.classList.add('chatboard__text');
    time.classList.add('chatboard__time');
    
    name.innerHTML = data.username;
    time.innerHTML = data.time;
    message.innerHTML = data.message;

    chatboard__content.appendChild(usericon);
    chatboard__content.appendChild(name);
    chatboard__content.appendChild(message);
    chatboard__content.appendChild(time);

    //親要素
    var list = document.querySelector('ul');

    list.appendChild(chatboard__content);

    let chatboard = document.getElementById("chatboard");
    window.scroll(0, chatboard.scrollHeight);

};

// チャットソケットにメッセージを送信
document.querySelector('.chat-message-submit').onclick = function(e) {
    const messageInput = document.querySelector('#chat-message-input');
    const message = messageInput.value;
    if(message.trim() !== ""){
        chatSocket.send(JSON.stringify({
            'user_id': user_id,
            'friend_id': friend_id,
            'message': message
        }));
    }
    messageInput.value = '';
};


// エンターキーでも送信できるように
document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('.chat-message-submit').click();
    }
};

// トークの表示を新しいものを下にしているため、最下にスクロールさせる
document.addEventListener("DOMContentLoaded", function () {
    let chatboard = document.getElementById("chatboard");
    window.scroll(0, chatboard.scrollHeight);
})