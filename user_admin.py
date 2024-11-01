from flask import *
import userdb

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        print(request.form)
        email = request.form['email']
        passwd = request.form['passwd']

        result = userdb.userDAO().authenicate(email,passwd)
        if result == None:
            flash("로그인 실패했습니다.")
            return redirect(url_for('login.login'))
        else:
            flash("로그인 성공했습니다.")
            session['userInfo'] = result
            return redirect(url_for('home'))
    else:
        return render_template('login/user.html')

@login_bp.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == "GET":
        return render_template('login/signup.html')
    else:
        print(request.form)
        email = request.form['email']
        passwd = request.form['passwd']
        name = request.form['name']
        nickname = request.form['nickname']
        auth = request.form['user_auth']
        if auth == '-1':
            flash("권한을 선택하세요")
            return redirect(url_for('login.signup'))
        ret_cnt = userdb.userDAO().create_user(email,passwd,name,nickname,auth)
        
        if ret_cnt:
            flash("회원 가입 성공했습니다.")
            return render_template('login/user.html')
        else:
            flash("회원 가입 실패했습니다.")
            return redirect(url_for('login.signup'))
        