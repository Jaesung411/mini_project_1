from flask import *
from chat import chat_bp
from user_admin import login_bp
from post import post_bp
from list import list_bp

app = Flask(__name__)
app.secret_key='1234'

app.register_blueprint(chat_bp)
app.register_blueprint(login_bp)
app.register_blueprint(post_bp)
app.register_blueprint(list_bp)

@app.route('/')
def welcome():
    return render_template('login/login.html')

@app.route('/home')
def home():
    print(session['userInfo'])
    return render_template('home.html')
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

if __name__ == '__main__':
    app.run(debug=True)