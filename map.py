from flask import *
from DB.storedb import StoreDAO

app = Flask(__name__)
app.secret_key='1234'

map_bp = Blueprint('map', __name__)

# 음식점 지도 페이지
@map_bp.route('/map/<store_id>')
def store_map(store_id):
    store = StoreDAO().get_store_by_id(store_id)

    name = store['name'] if store else None
    address = store['address'] if store else None
    
    print(name, address)

    return render_template('map/map.html', store_name=name, store_address=address)