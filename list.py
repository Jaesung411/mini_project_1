from flask import *
from storedb import *
from menudb import *
from imagedb import *

app = Flask(__name__)
app.secret_key='1234'

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

@app.route('/list_manage', methods=['GET', 'POST'])
def manage_stores():
    store_dao = StoreDAO()
    
    if request.method == 'POST':
        try:
            if 'action' in request.form and request.form['action'] == 'add':
                store_id = request.form['store_id']
                name = request.form['name']
                food_type = request.form['food_type']
                address = request.form['address']
                image = request.form['image']
                rate = request.form['rate']

                if store_dao.get_store_by_id(store_id):
                    flash('이미 존재하는 가게 번호입니다.')
                else:
                    store_dao.insert_store(store_id, name, address, image, rate, food_type)
                    flash('가게가 추가되었습니다.')

            elif 'action' in request.form and request.form['action'] == 'delete':
                store_id = request.form['store_id']
                store = store_dao.get_store_by_id(store_id)
                if store:
                    store_dao.delete_store(store_id)
                    flash('가게가 삭제되었습니다.')
                else:
                    flash('가게를 찾을 수 없습니다.')

            elif 'action' in request.form and request.form['action'] == 'update':
                store_id = request.form['store_id']
                name = request.form['name']
                food_type = request.form['food_type']
                address = request.form['address']
                image = request.form['image']
                rate = request.form['rate']

                store = store_dao.get_store_by_id(store_id)
                if store:
                    store_dao.update_store(store_id, name, address, image, rate, food_type)
                    flash('가게가 수정되었습니다.')
                else:
                    flash('가게를 찾을 수 없습니다.')

        except Exception as e:
            flash(f'오류가 발생했습니다: {str(e)}')

        return redirect(url_for('manage_stores'))  # 목록 페이지로 리다이렉트

    stores = store_dao.get_stores()
    return render_template('/list/list_manage.html', stores=stores)

if __name__ == '__main__':
    app.run(debug=True)