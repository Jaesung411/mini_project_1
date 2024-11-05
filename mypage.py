from flask import *
from DB.userdb import *

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

@mypage_bp.route('/delete_account',methods=['POST'])
def delete_accout():
    userDAO().delete_user(session['userInfo']['userId'])
    session.clear()
    return redirect(url_for("welcome"))