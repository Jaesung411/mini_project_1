from flask import *
from extensions import socketio #  home.py와 chat.py가 서로를 가져오면서 발생하는 순환 참조 문제 방지
from flask_socketio import SocketIO
from chat import chat_bp
from login import login_bp
from post import post_bp
from list import list_bp

app = Flask(__name__)
app.secret_key='1234'

socketio.init_app(app)  # app에 socketio 초기화

app.register_blueprint(chat_bp)
app.register_blueprint(login_bp)
app.register_blueprint(post_bp)
app.register_blueprint(list_bp)

@app.route('/')
def welcome():
    return render_template('welcome.html')

# @app.route('/login', methods=['GET','POST'])
# def login():
#     if request.method == "POST":
#         uemail = request.form['email']
#         passwd = request.form['passwd']
#         return render_template("home.html")
#     else:
#         return render_template('login/user.html')

# @app.route('/chat')
# def chat():
#     return render_template('chat/chat.html')

# @app.route('/post')
# def post():
#     return render_template('post/post.html')



# socketio.run으로 app이 동작하는 http 위에 socketio가 웹소켓으로 동작하도록 함
# chat_bp로 분리된 모듈에서 독립적으로 SocketIO 서버(WebSocket) 사용 불가
# 클라이언트에서 요청이 있어야 WebSocket 활성화되므로 평소에는 http로 통신함
if __name__ == '__main__':
    socketio.run(app, debug=True)