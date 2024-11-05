from flask import *
from DB.storedb import *
import DB.userdb as userdb
from werkzeug.utils import *

manage_bp = Blueprint('manage', __name__)

@manage_bp.route('/manage')
def manage():
    users = userdb.userDAO().get_users()
    stores = StoreDAO().get_stores() 
    return render_template('login/manage.html',users=users,stores=stores)

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

# 가게 추가
@manage_bp.route('/manage/add', methods=['POST'])
def add_store():
    # 클라이언트에서 넘어온 데이터 받기
    store_id = request.form.get('store_id')
    name = request.form.get('name')
    address = request.form.get('address')
    rate = request.form.get('rate')
    food_type = request.form.get('food_type')

    # 이미지 파일 처리
    image = request.files.get('image')  # 파일은 request.files로 가져옵니다.

    # 디버깅용 로그 추가
    print(f"Received data: store_id={store_id}, name={name}, address={address}, rate={rate}, food_type={food_type}")

    # 이미지 파일이 선택되었을 경우 처리
    if image:
        # 파일명 안전하게 처리
        filename = '1.png'  # 이미지는 항상 '1.png'로 저장
        store_folder = os.path.join(current_app.root_path, 'static', 'images', store_id)  # static/images/<store_id> 경로
        os.makedirs(store_folder, exist_ok=True)  # 폴더가 없으면 생성
        image_path = os.path.join(store_folder, filename)  # 저장될 경로 설정
        image.save(image_path)  # 이미지 파일을 지정된 경로에 저장
        print(f"Image saved to {image_path}")  # 디버깅용
    else:
        image_path = None  # 이미지가 없으면 None

    # StoreDAO 객체 생성
    store_dao = StoreDAO()

    # 가게 추가 전에 store_id가 이미 존재하는지 확인
    existing_store = store_dao.get_store_by_id(store_id)
    if existing_store:
        print(f"Error: store_id {store_id} already exists")
        # 클라이언트에게 실패 메시지와 함께 JSON 응답을 보냄
        return jsonify({"success": False, "message": "이 ID를 가진 가게가 이미 존재합니다."})

    try:
        # store_dao.insert_store에 image_path 전달
        store_dao.insert_store(store_id, name, address, image_path, rate, food_type)
        # 가게 추가 후 성공 메시지와 함께 JSON 응답을 보냄
        return jsonify({"success": True, "message": "가게가 성공적으로 추가되었습니다."})
    except Exception as e:
        print(f"Error while adding store: {e}")
        # 가게 추가 실패 시 실패 메시지와 함께 JSON 응답을 보냄
        return jsonify({"success": False, "message": "가게 추가에 실패했습니다."})

# 가게 수정
@manage_bp.route('/manage/edit/<int:store_id>', methods=['GET','POST'])
def edit_store(store_id):
    try:
        print("********************************")
        data = request.get_json()
        name = data.get('name')
        address = data.get('address')
        food_type = data.get('foodType')
        rate = data.get('rate')
        image = data.get('image', '')
        # DB에서 해당 가게 정보 수정
        store_dao = StoreDAO()
        success = store_dao.update_store(store_id, name, address, food_type, rate, image)
        
        if success:
            return jsonify({'success': True, 'message': '가게 정보가 수정되었습니다.'}), 200
        else:
            return jsonify({'success': False, 'message': '가게 수정 실패'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# 수정된 데이터베이스 업데이트 함수
def update_store(self, store_id, name, address, image, rate, food_type):
    cursor = DBConnect.get_db().cursor()
    sql_update = '''UPDATE store
                    SET name=%s, address=%s, image=%s, rate=%s, food_type=%s
                    WHERE store_id=%s'''
    ret_cnt = cursor.execute(sql_update, (name, address, image, rate, food_type, store_id))
    DBConnect.get_db().close()
    return f'update OK : {ret_cnt}'

# 가게 삭제
@manage_bp.route('/manage/delete/<int:store_id>', methods=['DELETE'])
def delete_store(store_id):
    store_dao = StoreDAO()
    try:
        store_dao.delete_store(store_id)
        return jsonify({'success': True, 'message': '가게가 삭제되었습니다.'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': '삭제 실패: ' + str(e)}), 500

@manage_bp.route('/manage/edit_data/<int:store_id>')
def edit_data(store_id):
    store_dao = StoreDAO()
    store = store_dao.get_store_by_id(store_id)
    print(store)
    if store:
        # store 객체에서 데이터를 추출하여 딕셔너리 형태로 반환
        return jsonify({
            'store_id': store['store_id'],
            'name': store['name'],
            'address': store['address'],
            'food_type': store['food_type'],
            'rate': store['rate'],
            'image': store['image']
        })
    else:
        # 가게가 존재하지 않으면 에러 반환
        return jsonify({'error': 'Store not found'}), 404
