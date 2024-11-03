from flask import *
from postdb import *

app = Flask(__name__)
app.secret_key = '1234'

@app.route('/<store_id>/reviews')
def review_list(store_id):
    review = ReviewDAO().get_reviews(store_id)
    print(review)
    return render_template('post/post.html', reviews=review)

if __name__ == '__main__':
    app.run(debug=True)