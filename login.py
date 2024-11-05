from flask import *
import DB.userdb

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        passwd = request.form['passwd']
        if userdb.userDAO().authenicate(email,passwd):
            flash("로그인 성공했습니다.")
            return render_template("home.html")
        else:
            flash("로그인 실패했습니다.")
            return redirect(url_for('login.login'))
    else:
        return render_template('login/user.html')

@login_bp.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == "POST":
        email = request.form['email']
        passwd = request.form['passwd']
        name = request.form['name']
        nickname = request.form['nickname']
        
        ret_cnt = userdb.userDAO().create_user(email,passwd,name,nickname)
        
        if ret_cnt:
            flash("회원 가입 성공했습니다.")
            return redirect(url_for('login.login'))
        else:
            flash("회원 가입 실패했습니다.")
            return redirect(url_for('login.signup'))
    else:
        return render_template('login/signup.html')