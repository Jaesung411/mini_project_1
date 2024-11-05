from flask import *
from DB.storedb import *
from DB.menudb import *
from DB.imagedb import *
from postdb import *

app = Flask(__name__)
app.secret_key='1234'

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

# if __name__ == '__main__':
#     app.run(debug=True)