from flask import *
from DB.storedb import *
from DB.menudb import *
from DB.imagedb import *
from DB.postdb import *

import os
import shutil  # 가게 삭제 시 폴더도 함께 삭제하는 기능을 하는 모듈
from werkzeug.utils import *

app = Flask(__name__)
app.secret_key='1234'

app.config['UPLOAD_FOLDER'] = 'static/images'

list_bp = Blueprint('list', __name__)

# @list_bp.route('/list')
# def list():
    # return render_template('list/list.html')

# # 홈 페이지
# @list_bp.route('/')
# def list():
#     list = StoreDAO().get_stores()
#     return render_template('list/list.html', list=list)

# 가게 상세 페이지
@list_bp.route('/<store_name>')
def store_detail(store_name):
    # store_name을 사용하여 해당 가게의 정보를 가져오는 로직 추가
    store = StoreDAO().get_store_by_name(store_name)
    # 가게 ID를 사용하여 이미지 가져오기
    images = ImageDAO().get_images_by_store_id(store['store_id'])
    # 해당 store_id의 메뉴 가져오기
    menus = MenuDAO().get_menus_by_store_id(store['store_id'])
    reviews = ReviewDAO().get_reviews(store['store_id'])

    page = request.args.get('page', 1, type=int)
    per_page = 9
    total_pages = (len(reviews) - 1) // per_page + 1
    paginated_reviews = reviews[(page - 1) * per_page: page * per_page]
    return render_template(
        'list/list_detail.html', 
        store=store, 
        images=images, 
        menus=menus, 
        reviews=reviews, 
        paginated_reviews=paginated_reviews, 
        page=page, 
        total_pages=total_pages
    )

# 메뉴 수정 페이지
@list_bp.route('/<store_name>/detail', methods=['GET', 'POST'])
def manage_menu(store_name):
    menu_dao = MenuDAO()
    store = StoreDAO().get_store_by_name(store_name)
    # store가 None인 경우 처리
    if store is None:
        flash(f"{store_name}에 해당하는 가게를 찾을 수 없습니다.")
        return redirect('/home')
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
        else:
            menu_id = request.form.get('menu_id')
            menu_name = request.form.get('menu_name')
            menu_price = request.form.get('price')
            
            menu_dao.update_menu(menu_id,store_id,menu_name,menu_price)
    images = ImageDAO().get_images_by_store_id(store_id)
    menus = MenuDAO().get_menus_by_store_id(store_id)
    return render_template('list/store_detail.html', store=store, images=images, menus=menus)

# 이미지 수정 페이지
@list_bp.route('/<store_name>/image', methods=['GET', 'POST'])
def manage_images(store_name):
    image_dao = ImageDAO()
    store = StoreDAO().get_store_by_name(store_name)
    
    # store가 None인 경우 처리
    if store is None:
        flash(f"{store_name}에 해당하는 가게를 찾을 수 없습니다.")
        return redirect('/home')
    
    store_id = store['store_id']

    if request.method == 'POST':
        action = request.form.get('action')  # action 변수를 여기서 초기화
        
        if action == '추가':
            if 'image' in request.files:
                image_file = request.files['image']
                image_id = image_dao.get_max_image_id() + 1  # ID는 DB에서 최대값을 가져와서 생성
                # 이미지가 저장될 폴더 경로
                image_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(store_id))

                # 폴더가 존재하지 않으면 생성
                if not os.path.exists(image_folder):
                    os.makedirs(image_folder)

                upload_folder = app.config['UPLOAD_FOLDER']
                path = f"/{upload_folder}/{store_id}/{image_file.filename}" 
                image_file.save(os.path.join(image_folder, image_file.filename))  # 이미지 저장
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

                # 폴더가 존재하지 않으면 생성
                if not os.path.exists(image_folder):
                    os.makedirs(image_folder)

                file_path = os.path.join(image_folder, f'{image_id}.png')  # 예: 1.png, 2.png 등
                image_file.save(file_path)
                path = f'{store_id}/{image_id}.png'
                image_dao.update_image(image_id, store_id, path)
                flash('이미지가 수정되었습니다.')
    
    # 이미지 경로 처리
    images = image_dao.get_images_by_store_id(store_id)
    # 이미지를 images/<store_id>/<image_name> 형식으로 처리
    for image in images:
        image['path'] = f'images/{store_id}/{image["path"].split("/")[1]}'
    
    return render_template('list/store_detail.html', store=store, images=images)