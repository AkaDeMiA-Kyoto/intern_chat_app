
console.log(location.pathname.split('/')[2]);
console.log(location.pathname.split('/')[3]);

var pathname1 = location.pathname.split('/')[2];
var pathname2 = location.pathname.split('/')[3];

if (pathname1 > pathname2){
    var room_id1 = pathname1;
    var room_id2 = pathname2;
}else {
    var room_id1 = pathname2;
    var room_id2 = pathname1;
}

const talkSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/talk_room/'
    + room_id1
    + '/'
    + room_id2
    + '/'
);

talkSocket.onmessage = function(e){
    const data = JSON.parse(e.data);
    document.getElementById('').value += data.message

};

talkSocket.onclose = function(e){
    console.error('Talk socket closed unexpectedly');
};


//送信ボタンクリック時
document.querySelector('#submit').onclick = function(e){
    const messageInputDom = document.querySelector('#submit');
    const message = messageInputDom.value;
    talkSocket.send(JSON.stringify({
        'message':message
    }));
    messageInputDom.value = '';
};

