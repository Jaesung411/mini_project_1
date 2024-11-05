from flask import *
from postdb import *
from DB.storedb import *
from DB.menudb import *
from DB.imagedb import *
from werkzeug.utils import secure_filename
import os
from datetime import datetime

post_bp = Blueprint('post', __name__)
post_bp.secret_key = '1234'

@post_bp.route('/<store_id>/reviews')
def review_list_detail(store_id):
    review = ReviewDAO().get_reviews(store_id)
    print(review)
    return render_template('post/post.html', reviews=review)

@post_bp.route('/<user_id>/myreview')
def my_review_list(user_id):
    review = ReviewDAO().get_my_reviews(user_id)
    return render_template('post/post.html', reviews=review)

@post_bp.route('/<store_id>/rate')
def store_rate(store_id):
    review = ReviewDAO().get_rate(store_id)
    return f'update OK : {review}'

# 파일 업로드 설정
UPLOAD_FOLDER = 'static/reviewImg'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@post_bp.route('/new_review/<int:store_id>/<int:page>', methods=['POST'])
def add_review(store_id, page):
    try:
        # 로그인 확인
        if 'userInfo' not in session:
            flash('로그인이 필요한 서비스입니다.', 'error')
            return redirect(url_for('auth.login'))

        user_id = session['userInfo'].get('userId')
        
        # 입력값 검증
        contents = request.form.get('contents')
        rate = request.form.get('rate')
        
        if not contents or not rate:
            flash('리뷰 내용과 평점을 모두 입력해주세요.', 'error')
            return redirect(url_for('store.view_store', store_id=store_id, page=page))
        
        # 평점 검증 (0-5 사이의 값)
        try:
            rate = float(rate)
            if not 0 <= rate <= 5:
                raise ValueError
        except ValueError:
            flash('올바른 평점을 입력해주세요.', 'error')
            return redirect(url_for('store.view_store', store_id=store_id, page=page))

        # 이미지 처리
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                # 파일명 안전하게 만들기
                filename = secure_filename(file.filename)
                # 파일명에 타임스탬프 추가하여 중복 방지
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                
                # 업로드 폴더가 없다면 생성
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)
                
                # 파일 저장
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                image_path = f'../../static/reviewImg/{filename}'

        # 리뷰 저장
        reviews = ReviewDAO.insert_review(
            user_id=user_id,
            store_id=store_id,
            contents=contents,
            rate=rate,
            image=image_path
        )

        # 가게 정보 조회
        store = StoreDAO().get_store_by_id(store_id)
        images = ImageDAO().get_images_by_store_id(store_id)
        menus = MenuDAO().get_menus_by_store_id(store_id)

        # 페이지네이션 처리
        per_page = 9
        total_reviews = len(reviews)
        total_pages = (total_reviews - 1) // per_page + 1
        
        # 페이지 번호 검증
        page = max(1, min(page, total_pages))
        
        # 현재 페이지의 리뷰만 선택
        start_idx = (page - 1) * per_page
        paginated_reviews = reviews[start_idx:start_idx + per_page]

        flash('리뷰가 성공적으로 등록되었습니다.', 'success')
        
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

    except Exception as e:
        flash('리뷰 등록 중 오류가 발생했습니다. 다시 시도해주세요.', 'error')
        return redirect(url_for('store.view_store', store_id=store_id, page=page))

@post_bp.route('/update/<int:store_id>/<int:review_id>/<int:page>', methods=['POST'])
def update_review(store_id, review_id, page):
    image = request.form.get('image')
    reviews = ReviewDAO.update_review(request.form['contents'], request.form['rate'], review_id, store_id, image)
    
    store = StoreDAO().get_store_by_id(store_id)
    images = ImageDAO().get_images_by_store_id(store_id)
    menus = MenuDAO().get_menus_by_store_id(store_id)
    reviews = ReviewDAO().get_reviews(store_id)

    per_page = 9
    total_pages = (len(reviews) - 1) // per_page + 1
    paginated_reviews = reviews[(page - 1) * per_page: page * per_page]  # 해당 페이지의 리뷰만 가져오기

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


@post_bp.route('/delete/<int:store_id>/<int:review_id>/<int:page>', methods=['POST'])
def delete_review(store_id, review_id,page):
    reviews = ReviewDAO.delete_review(review_id, store_id)
    store = StoreDAO().get_store_by_id(store_id)
    images = ImageDAO().get_images_by_store_id(store_id)
    menus = MenuDAO().get_menus_by_store_id(store_id)
    reviews = ReviewDAO().get_reviews(store_id)

    per_page = 9
    total_pages = (len(reviews) - 1) // per_page + 1
    paginated_reviews = reviews[(page - 1) * per_page: page * per_page]  # 해당 페이지의 리뷰만 가져오기

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
#     post_bp.run(debug=True)