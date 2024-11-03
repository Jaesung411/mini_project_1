from flask import *
import userdb
from werkzeug.security import* 

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        # print(request.form)
        email = request.form['email']
        passwd = request.form['passwd']

        #이메일에 해당하는 회원 정보
        user_info = userdb.userDAO().authenicate(email)

        if not check_password_hash(user_info[2], passwd):
            flash("로그인 실패했습니다.")
            return redirect(url_for('login.login'))
        else:
            flash("로그인 성공했습니다.")
            session['userInfo'] = {
                'email':user_info[1],
                'name':user_info[3],
                'nickname':user_info[4],
                'role':user_info[5]
            }
            return redirect(url_for('home'))
    else:
        return render_template('login/login.html')

@login_bp.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == "GET":
        return render_template('login/signup.html')
    else:
        # print(request.form)
        email = request.form['email']
        passwd = request.form['passwd']
        name = request.form['name']
        nickname = request.form['nickname']
        auth = request.form['user_auth']

        #비밀번호 암호화 
        hashed_password = generate_password_hash(passwd)
        
        if auth == '-1':
            flash("권한을 선택하세요")
            return redirect(url_for('login.signup'))
        ret = userdb.userDAO().create_user(email,hashed_password,name,nickname,auth)
      
        if ret[0]:
            flash(ret[1])
            return redirect(url_for('login.login'))
        
        else:
            flash(ret[1])
            return render_template('login/signup.html')
        