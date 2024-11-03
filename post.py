from flask import *
from postdb import *

app = Flask(__name__)
app.secret_key = '1234'

@app.route('/<store_id>/reviews')
def review_list(store_id):
    review = ReviewDAO().get_reviews(store_id)
    return render_template('post/post.html', reviews=review)

@app.route('/new_review', methods=['POST'])
def add_review():
    user_id = 1
    store_id = 1
    review = ReviewDAO.insert_review( user_id, store_id, request.form['contents'], request.form['rate'], request.form['image'])
    return render_template('post/post.html', reviews=review)

if __name__ == '__main__':
    app.run(debug=True)