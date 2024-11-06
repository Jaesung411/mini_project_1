from flask import *
import DB.userdb as userdb
from werkzeug.security import* 

import logging
import logging.config 

# 로깅 설정
logging.config.fileConfig('logging.conf')
logging.getLogger('werkzeug').disabled=True
# logger = logging.getLogger(__name__)
bp_logger = logging.getLogger(__name__ + '.login_bp')
bp_logger.info('111111111111')
login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET','POST'])
def login():
    print('>>>>>>>>>>>>>>>')

    bp_logger.info("로그인 필요")
    

    if request.method == "POST":
        # print(request.form)
        email = request.form['email']
        passwd = request.form['passwd']

        #이메일에 해당하는 회원 정보
        user_info = userdb.userDAO().authenicate(email)

        if user_info == None or not check_password_hash(user_info[2], passwd):
            bp_logger.info("로그인 실패")
            flash("로그인 실패했습니다.")
            return redirect(url_for('login.login'))
        else:
            flash("로그인 성공했습니다.")
            session['userInfo'] = {
                'userId':user_info[0],
                'email':user_info[1],
                'name':user_info[4],
                'nickname':user_info[3],
                'role':user_info[5]
            }
            bp_logger.info("로그인 성공 홈으로")
            bp_logger.info("user_id : {user_info[0]}")
            return redirect(url_for('home'))
    else:
        bp_logger.info('/login 진입...')
        bp_logger.info('...')

        print('>>>>>>>>>>>>>>>')

        return render_template('login/login.html')

@login_bp.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == "GET":
        bp_logger.info("회원가입 시도")
        return render_template('login/signup.html')
    else:
        # print(request.form)
        email = request.form['email']
        passwd = request.form['passwd']
        name = request.form['name']
        nickname = request.form['nickname']
        # auth = request.form['user_auth']
        auth = 1

        #비밀번호 암호화 
        hashed_password = generate_password_hash(passwd)
        
        ret = userdb.userDAO().create_user(email,hashed_password,nickname,name,auth)
        if ret[0]:
            bp_logger.info("{name} 님 회원가입 성공")
            flash(ret[1])
            return redirect(url_for('login.login'))
        else:
            bp_logger.info("회원가입 실패")
            flash(ret[1])
            return render_template('login/signup.html')

@login_bp.route('/logout')    
def logout():
    bp_logger.info("로그아웃")
    session.pop('login_info', None)
    return redirect(url_for('login.login'))

        