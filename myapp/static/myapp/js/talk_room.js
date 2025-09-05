const roomName = document.getElementById('room-name').value;
const user_id = document.getElementById('user-id').value;
const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/" + roomName + "/")
console.log("ws://" + window.location.host + "/ws/chat/" + roomName + "/")

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    if ("error" in data) {
        console.warn(data.error);
        return;
    }

    createNewMessage(data.message);
    console.log(data);
}

chatSocket.onclose = () => {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#submit-btn').onclick = function (e) {
    e.preventDefault();

    if (!chatSocket || chatSocket.readyState !== WebSocket.OPEN) {
        console.error('WebSocket is not open. readyState=' + chatSocket.readyState);
        return;
    }

    const messageDom = document.getElementById('talk_field');
    const message = messageDom.value;

    if (message === '') return;

    try {
        chatSocket.send(JSON.stringify({ "message": message, "user_id": user_id }))
        messageDom.value = '';
    } catch (error) {
        console.error('Error sending message:', error);
    }
}

function createNewMessage(message) {
    const parentNode = document.getElementById("chatboard");

    const li = document.createElement("li");
    li.classList.add("chatboard__content");
    li.classList.add("chatboard__content--friend");

    const messageText = document.createElement("p");
    messageText.textContent = message.talk;

    messageText.classList.add("chatboard__text");

    const messageFromText = document.createElement("p");
    messageFromText.textContent = message.message_from;

    messageFromText.classList.add("chatboard__name");

    li.appendChild(messageFromText);
    li.appendChild(messageText);
    parentNode.appendChild(li);
}