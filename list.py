from flask import *
from storedb import *
from menudb import *
from imagedb import *
import os
import shutil  # 가게 삭제 시 폴더도 함께 삭제하는 기능을 하는 모듈
from werkzeug.utils import *

app = Flask(__name__)
app.secret_key='1234'

# 업로드 폴더 설정
UPLOAD_FOLDER = 'static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 홈 페이지
@app.route('/')
def list():
    stores = StoreDAO().get_stores()
    return render_template('list/list.html', list=stores)

# 가게 상세 페이지
@app.route('/<store_name>')
def store_detail(store_name):
    store = StoreDAO().get_store_by_name(store_name)
    images = ImageDAO().get_images_by_store_id(store['store_id'])
    menus = MenuDAO().get_menus_by_store_id(store['store_id'])
    return render_template('list/list_detail.html', store=store, images=images, menus=menus)

# 가게 관리 페이지
@app.route('/list_manage', methods=['GET', 'POST'])
def manage_stores():
    store_dao = StoreDAO()
    action = None
    store = None  # store 변수를 초기화

    if request.method == 'POST':
        try:
            action = request.form.get('action')
            store_id = request.form.get('store_id')
            name = request.form.get('name')
            food_type = request.form.get('food_type')
            address = request.form.get('address')
            rate = request.form.get('rate')
            # 이미지를 저장할 경로 설정
            image_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'images', store_id)
            if not os.path.exists(image_folder):
                os.makedirs(image_folder)

            if action == 'add':
                image = request.files['image']
                image.save(os.path.join(image_folder, '1.png'))  # 첫 번째 이미지로 저장
                store_dao.insert_store(store_id, name, address, f'images/{store_id}/1.png', rate, food_type)
                flash('가게가 추가되었습니다.')
            elif action == 'delete':
                store = store_dao.get_store_by_id(store_id)
                if store:
                    # 이미지 폴더 삭제
                    if os.path.exists(image_folder):
                        shutil.rmtree(image_folder)  # 폴더와 그 내용을 모두 삭제
                    store_dao.delete_store(store_id)
                    flash('가게가 삭제되었습니다.')
                else:
                    flash('가게를 찾을 수 없습니다.')
            elif action == 'update':
                # 이미지가 수정된 경우
                if 'image' in request.files and request.files['image']:
                    image = request.files['image']
                    image.save(os.path.join(image_folder, '1.png'))  # 첫 번째 이미지로 저장
                store = store_dao.get_store_by_id(store_id)
                if store:
                    store_dao.update_store(store_id, name, address, f'images/{store_id}/1.png', rate, food_type)
                    flash('가게가 수정되었습니다.')
                else:
                    flash('가게를 찾을 수 없습니다.')
        except Exception as e:
            flash(f'오류가 발생했습니다: {str(e)}')

        return redirect(url_for('manage_stores'))  # 목록 페이지로 리다이렉트

    stores = store_dao.get_stores()
    return render_template('/list/list_manage.html', stores=stores, store=store)

@app.route('/<store_name>/detail', methods=['GET', 'POST'])
def manage_menu(store_name):
    menu_dao = MenuDAO()
    store = StoreDAO().get_store_by_name(store_name)
    store_id = store['store_id']
    
    if request.method == 'POST':
        action = request.form.get('action')

        if action == '추가':
            menu_name = request.form.get('menu_name')
            price = request.form.get('price')
            max_menu_id = menu_dao.get_max_menu_id() + 1
            menu_dao.insert_menu(max_menu_id, store_id, menu_name, price)
            flash('메뉴가 추가되었습니다.')

        elif action == '삭제':
            menu_id = request.form.get('menu_id')
            menu_dao.delete_menu(menu_id)
            flash('메뉴가 삭제되었습니다.')

    images = ImageDAO().get_images_by_store_id(store_id)
    menus = MenuDAO().get_menus_by_store_id(store_id)

    return render_template('list/store_detail.html', store=store, images=images, menus=menus)

def generate_new_image_filename(image, folder):
    base, extension = os.path.splitext(secure_filename(image.filename))
    i = 1
    new_filename = f"{base}{extension}"
    
    # 중복 파일 이름 확인
    while os.path.exists(os.path.join(folder, new_filename)):
        new_filename = f"{base}_{i}{extension}"
        i += 1
    
    return new_filename

@app.route('/<store_name>/image', methods=['GET', 'POST'])
def manage_images(store_name):
    image_dao = ImageDAO()
    store = StoreDAO().get_store_by_name(store_name)
    store_id = store['store_id']

    if request.method == 'POST':
        action = request.form.get('action')  # action 변수를 여기서 초기화

        if action == '추가':
            if 'image' in request.files:
                image_file = request.files['image']
                image_id = image_dao.get_max_image_id() + 1  # ID는 DB에서 최대값을 가져와서 생성
                path = f'images/{store_id}/{image_file.filename}'  # 저장할 경로 설정
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], path))  # 이미지 저장
                image_dao.insert_image(store_id, path)  # 수정된 메서드 호출
                flash('이미지가 추가되었습니다.')
        
        elif action == '삭제':
            image_id = request.form.get('image_id')
            image_dao.delete_image(image_id)
            flash('이미지가 삭제되었습니다.')

        elif action == '수정':
            image_id = request.form.get('image_id')
            if 'image' in request.files:
                image_file = request.files['image']
                image_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(store_id))
                if not os.path.exists(image_folder):
                    os.makedirs(image_folder)

                file_path = os.path.join(image_folder, f'{image_id}.png')  # 예: 1.png, 2.png 등
                image_file.save(file_path)
                path = f'{store_id}/{image_id}.png'
                image_dao.update_image(image_id, store_id, path)
                flash('이미지가 수정되었습니다.')

    images = image_dao.get_images_by_store_id(store_id)
    return render_template('list/store_image.html', store=store, images=images)

if __name__ == '__main__':
    app.run(debug=True)