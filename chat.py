from flask import *
from extensions import socketio #  home.py와 chat.py가 서로를 가져오면서 발생하는 순환 참조 문제 방지
from flask_socketio import SocketIO, join_room, leave_room, send
from datetime import datetime
from DB.messagedb import MessageDAO

chat_bp = Blueprint('chat', __name__)
message_dao = MessageDAO()

@chat_bp.route('/chat')
def chat():
    return render_template('chat/chat.html')

@socketio.on('join')  # 페이지 로드 시 방 입장 이벤트
def on_join(data):
    room = data['room']
    join_room(room)
    print(f"{request.sid} 입장 완료")

@socketio.on('message')  # 클라이언트의 메시지 전송 요청 처리 이벤트
def handle_message(data):
    room = 'chatroom'
    user_id = session['userInfo']['userId']
    name = session['userInfo']['nickname']
    contents = data['contents']
    timestamp = datetime.now()

    # 데이터베이스에 메시지 저장
    message_dao.insert_message(
        user_id=user_id,
        name=name,
        contents=contents,
        timestamp=timestamp
    )

    print(f"{name}: {contents}")
    # 모든 사용자에게 메시지 전송
    socketio.emit('message', f"{name}: {contents}", room=room)

@socketio.on('leave')  # 방 퇴장 이벤트
def handle_leave(data):
    room = 'chatroom'
    name = data['name']
    leave_room(room)
    print(f"{name} 퇴장 완료")
    send(f"{name} has left the room.", room=room)

@socketio.on('get_messages')  # 이전 메시지 요청 이벤트
def get_messages():
    room = 'chatroom'
    messages = message_dao.get_messages()[:10]
    for message in messages:
        name = message['name']
        contents = message['contents']
        socketio.emit('get_messages', f"{name}: {contents}", room=room)

@socketio.on('update_message')  # 메시지 업데이트 이벤트
def update_message(data):
    message_id = data['message_id']
    new_content = data['new_content']
    message_dao.update_message(message_id, new_content)
    send(f"Message {message_id} updated.", room='chatroom')

@socketio.on('delete_message')  # 메시지 삭제 이벤트
def delete_message(data):
    message_id = data['message_id']
    message_dao.delete_message(message_id)
    send(f"Message {message_id} deleted.", room='chatroom')