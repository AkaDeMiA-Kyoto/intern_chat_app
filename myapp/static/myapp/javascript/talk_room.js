
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
    var time 
    var p1 = document.createElement('p');
    var sender = document.createTextNode(data.sender);
    p1.appendChild(sender);
    var p2 = document.createElement('p');
    var content = document.createTextNode(data.message);
    p2.appendChild(content);
    var h = document.createElement('h6');
    var date = document.createTextNode(data.time);
    h.appendChild(date);
    h.style = "text-align: right;";
    var hr = document.createElement('hr');
    var talk_append = document.getElementById('talk_append');
    talk_append.appendChild(p1);
    talk_append.appendChild(p2);
    talk_append.appendChild(h);
    talk_append.appendChild(hr);


};

talkSocket.onclose = function(e){
    console.error('Talk socket closed unexpectedly');
};


//送信ボタンクリック時
document.querySelector('#submit').onclick = function(e){
    const messageInputDom = document.querySelector('#id_content');
    const message = messageInputDom.value;
    console.log(message);
    talkSocket.send(JSON.stringify({
        'message':message,
        'friend_id': pathname2
    }));
    messageInputDom.value = '';
};

