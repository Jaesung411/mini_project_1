from flask import *
from DB.userdb import *
from werkzeug.security import check_password_hash, generate_password_hash
mypage_bp = Blueprint('mypage', __name__)

@mypage_bp.route('/update_profile',methods=['POST'])
def update_profile():
    name = request.form.get('name')
    email = request.form.get('email')
    nickname = request.form.get('nickname')

    # 사용자 정보 업데이트
    try:
        userDAO().update_user(session['userInfo']['userId'], email, name, nickname)
        session['userInfo']['name'] = name
        session['userInfo']['email'] = email
        session['userInfo']['nickname'] = nickname
        flash("프로필이 성공적으로 업데이트되었습니다.", "success")  # 성공 메시지 전달
    except Exception as e:
        flash("프로필 업데이트에 실패했습니다. 다시 시도해 주세요.", "danger")  # 실패 메시지 전달
        print(f"Error updating profile: {e}")

    return redirect(url_for("manage.mypage"))

@mypage_bp.route('/update_pwd',methods=['POST'])
def update_pwd():
    input_current_pwd = request.form['current_password']
    new_pwd = request.form['new_password']
    confirm_pwd = request.form['confirm_new_password']

    userinfo = userDAO().authenicate(session['userInfo']['email'])
    cpwd = userinfo[2]

    if not check_password_hash(cpwd, input_current_pwd):
        flash("현재 비밀번호와 다릅니다.")
    else:
        if new_pwd != confirm_pwd:
            flash("확인 비밀번호가 다릅니다.")
        else:
            new_hashed_password = generate_password_hash(new_pwd)
            userDAO().update_pwd(session['userInfo']['userId'],new_hashed_password)


    # return redirect(url_for("welcome"))
    return redirect(url_for("manage.mypage"))

@mypage_bp.route('/delete_account',methods=['POST'])
def delete_accout():
    userDAO().delete_user(session['userInfo']['userId'])
    session.clear()
    return redirect(url_for("welcome"))