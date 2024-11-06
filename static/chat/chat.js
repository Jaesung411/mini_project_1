document.addEventListener("DOMContentLoaded", () => {
    const socket = io();  // 소켓 연결
    const chatBox = document.getElementById("messages");
    const messageForm = document.getElementById("message-form");
    const messageInput = document.getElementById("message-input");

    // DOM 확인
    if (!chatBox || !messageForm || !messageInput) {
        console.error("DOM 요소 전달 실패");
        return;
    }

    // 방 입장 요청
    socket.emit('join', { room: 'chatroom' });

    // 페이지 로드 시 이전 메시지 요청
    socket.emit('get_messages');

    // 메시지 수신 이벤트
    socket.on('message', (msg) => {
        console.log("Message received from server:", msg);
        displayMessage(msg);
    });

    // 메시지 표시 함수
    function displayMessage(message) {
        if (typeof message !== 'string') {
            console.error("Received message is not a string:", message);
            return;  // 문자열인지 확인
        }

        const messageElement = document.createElement("div");
        messageElement.classList.add("chat-message");
        messageElement.innerText = message; // 메시지 내용 설정
        chatBox.prepend(messageElement); // 최신 메시지가 위로 쌓이게 함
    }

    // 메시지 전송 이벤트
    messageForm.addEventListener("submit", (event) => {
        event.preventDefault();  // 폼 제출 방지
        const messageContent = messageInput.value;  // 입력한 메시지 가져오기
        if (messageContent) {
            // 메시지 전송
            socket.emit('message', {
                contents: messageContent,
            });
            messageInput.value = "";  // 입력 필드 초기화
        }
    });
});