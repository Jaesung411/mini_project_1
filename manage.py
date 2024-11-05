from flask import *
import DB.userdb as userdb

manage_bp = Blueprint('manage', __name__)

@manage_bp.route('/manage')
def manage():
    users = userdb.userDAO().get_users()
    return render_template('login/manage.html',users=users)

@manage_bp.route('/mypage')
def mypage():
    return render_template('login/mypage.html')

@manage_bp.route('/update_member/<int:userId>', methods=['POST'])
def update_member(userId):
    try:
        data = request.get_json()
        email = data.get('email')
        name = data.get('name')
        nickname = data.get('nickname')
        
        userdb.userDAO().update_user(userId, email, nickname, name)
        # 성공/실패 여부를 반환
        return jsonify({'success': True})
    except Exception as e:
        print("Error : " + e)
        jsonify({'success': False})
    

@manage_bp.route('/delete_member/<int:userId>', methods=['DELETE'])
def delete_member(userId):
    # 데이터베이스에서 해당 회원의 정보를 삭제하는 로직 추가
    try:
        userdb.userDAO().delete_user(userId)
        # 삭제 성공 시 반환
        return jsonify({'success': True})
    except Exception as e:
            print("Error : " + e)
            jsonify({'success': False})