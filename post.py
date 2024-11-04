from flask import *
from postdb import *
from DB.storedb import *
from DB.menudb import *
from DB.imagedb import *

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

@post_bp.route('/new_review/<int:store_id>', methods=['POST'])
def add_review(store_id):
    user_id = session['userInfo']['userId']
    review = ReviewDAO.insert_review( user_id, store_id, request.form['contents'], request.form['rate'], request.form['image'])
    store = StoreDAO().get_store_by_id(store_id)
    images = ImageDAO().get_images_by_store_id(store_id)
    menus = MenuDAO().get_menus_by_store_id(store_id)
    return render_template('list/list_detail.html', store=store, images=images, menus=menus, reviews=review)

@post_bp.route('/update/<int:store_id>/<int:review_id>', methods=['POST'])
def update_review(store_id, review_id):
    review = ReviewDAO.update_review(request.form['contents'], request.form['rate'], review_id, store_id, request.form['image'])
    store = StoreDAO().get_store_by_id(store_id)
    images = ImageDAO().get_images_by_store_id(store_id)
    menus = MenuDAO().get_menus_by_store_id(store_id)
    return render_template('list/list_detail.html', store=store, images=images, menus=menus, reviews=review)

@post_bp.route('/delete/<int:store_id>/<int:review_id>', methods=['POST'])
def delete_review(store_id, review_id):
    review = ReviewDAO.delete_review(review_id, store_id)
    store = StoreDAO().get_store_by_id(store_id)
    images = ImageDAO().get_images_by_store_id(store_id)
    menus = MenuDAO().get_menus_by_store_id(store_id)
    return render_template('list/list_detail.html', store=store, images=images, menus=menus, reviews=review)


# if __name__ == '__main__':
#     post_bp.run(debug=True)