from flask import *
from postdb import *

# post_bp = Flask(__name__)
post_bp = Blueprint('post', __name__)
post_bp.secret_key = '1234'

@post_bp.route('/<store_id>/reviews')
def review_list(store_id):
    review = ReviewDAO().get_reviews(store_id)
    return render_template('post/post.html', reviews=review)

@post_bp.route('/new_review', methods=['POST'])
def add_review():
    user_id = 1
    store_id = 1
    review = ReviewDAO.insert_review( user_id, store_id, request.form['contents'], request.form['rate'], request.form['image'])
    return render_template('post/post.html', reviews=review)

@post_bp.route('/update', methods=['POST'])
def update_review():
    review_id = 1
    store_id = 1
    review = ReviewDAO.update_review(request.form['contents'], request.form['rate'], review_id, store_id, request.form['image'])
    return render_template('post/post.html', reviews=review)

@post_bp.route('/delete', methods=['GET'])
def delete_review():
    review_id = 1
    store_id = 1
    review = ReviewDAO.delete_review(review_id, store_id)
    return render_template('post/post.html', reviews=review)


if __name__ == '__main__':
    post_bp.run(debug=True)