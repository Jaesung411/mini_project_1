from flask import *
from extensions import socketio #  home.py와 chat.py가 서로를 가져오면서 발생하는 순환 참조 문제 방지
from flask_socketio import SocketIO, join_room, leave_room, send
from datetime import datetime
from messagedb import MessageDAO

chat_bp = Blueprint('chat', __name__)
message_dao = MessageDAO()

@chat_bp.route('/chat')
def chat():
    return render_template('chat/chat.html')