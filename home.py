from flask import *
from extensions import socketio #  home.py와 chat.py가 서로를 가져오면서 발생하는 순환 참조 문제 방지
from flask_socketio import SocketIO
from chat import chat_bp
from user_admin import login_bp
from post import post_bp
from manage import manage_bp
from mypage import mypage_bp
from map import map_bp
from list import list_bp

from DB.storedb import *
from DB.menudb import *
from DB.imagedb import *
from DB.postdb import *
import logging
import logging.config 

# # 로깅 설정
# logging.config.fileConfig('logging.conf')
# logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key='1234'

app.config['UPLOAD_FOLDER'] = 'static/images'

socketio.init_app(app)  # app에 socketio 초기화

app.register_blueprint(chat_bp)
app.register_blueprint(login_bp)
app.register_blueprint(post_bp)
app.register_blueprint(manage_bp)
app.register_blueprint(mypage_bp)
app.register_blueprint(map_bp)
app.register_blueprint(list_bp)

@app.route('/')
def welcome():
    return render_template('login/login.html')

@app.route('/home')
def home():

    # 페이지 번호와 페이지당 항목 수 설정
    page = int(request.args.get('page', 1))
    per_page = 8  # 페이지당 가게 수
    
    # 전체 가게 리스트 가져오기 (데이터베이스에서 가져와야 합니다)
    all_stores = StoreDAO().get_stores()
    
    # 현재 페이지에 해당하는 가게 목록만 가져오기
    start = (page - 1) * per_page
    end = start + per_page
    paginated_stores = all_stores[start:end]
    print(paginated_stores)
    # 전체 페이지 수 계산
    total_pages = (len(all_stores) + per_page - 1) // per_page
    
    return render_template('home.html', list=paginated_stores, page=page, total_pages=total_pages)
    # return render_template('home.html', list=list)



@app.route('/search')
def search():
    query = request.args.get('query')
    stores = StoreDAO().get_stores()
    if query:
        # 데이터베이스나 데이터 리스트에서 검색어가 포함된 가게를 필터링합니다.
        filtered_list = [store for store in stores if query.lower() in store['name'].lower()]
    else:
        filtered_list = stores  # 검색어가 없을 경우 전체 목록 반환
        # 페이지네이션 처리가 필요할 경우 추가
      
    page = request.args.get('page', 1, type=int)
    per_page = 8
    total_pages = (len(filtered_list) - 1) // per_page + 1
    paginated_list = filtered_list[(page - 1) * per_page: page * per_page]

    return render_template(
        'home.html',
        list=paginated_list,
        page=page,
        total_pages=total_pages
    )

# socketio.run으로 app이 동작하는 http 위에 socketio가 웹소켓으로 동작하도록 함
# chat_bp로 분리된 모듈에서 독립적으로 SocketIO 서버(WebSocket) 사용 불가
# 클라이언트에서 요청이 있어야 WebSocket 활성화되므로 평소에는 http로 통신함
if __name__ == '__main__':
    socketio.run(app, debug=True)