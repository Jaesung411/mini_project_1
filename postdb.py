import pymysql
from DB.storedb import *

class DBConnect:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def get_db(self):
        return pymysql.connect(
            host='127.0.0.1',
            user='user1',
            passwd='qwer1234',
            db='mini_proj',
            charset='utf8',
            autocommit=True
        )

class ReviewDAO:
    # 가게 별 리뷰 조회
    @staticmethod
    def get_reviews(store_id):
        ret = []
        cursor = DBConnect.get_db().cursor()

        sql_select = 'SELECT REVIEW_ID, CONTENTS, RATE, IMAGE FROM REVIEW WHERE store_id = %s ORDER BY REVIEW_ID DESC'
        cursor.execute(sql_select, (store_id,))

        rows = cursor.fetchall()
        for row in rows:
            ret.append({
                'review_id': row[0],
                'contents': row[1],
                'rate': row[2],
                'image': row[3]
            })
        return ret
    
    # 내가 작성한 리뷰 조회
    @staticmethod
    def get_my_reviews(user_id):
        
        ret = []
        cursor = DBConnect.get_db().cursor()

        sql_select = 'SELECT REVIEW_ID, CONTENTS, RATE, IMAGE FROM REVIEW WHERE USER_ID = %s ORDER BY REVIEW_ID DESC'
        cursor.execute(sql_select, (user_id))

        rows = cursor.fetchall()
        for row in rows:
            ret.append({
                'review_id': row[0],
                'contents': row[1],
                'rate': row[2],
                'image': row[3]
            })
        return ret
    
    # 가게 평점 계산
    @staticmethod
    def get_rate(store_id):
        
        ret = []
        cursor = DBConnect.get_db().cursor()

        sql_select = 'SELECT ROUND(AVG(RATE),1) FROM REVIEW WHERE STORE_ID = %s ORDER BY REVIEW_ID DESC'
        cursor.execute(sql_select, (store_id,))

        rate = cursor.fetchone()
        return rate[0] if rate[0] is not None else 0
    
    # 새 리뷰 생성
    @staticmethod
    def insert_review(user_id, store_id, contents, rate, image=None):
        print(f'store_id: {store_id}')  # 디버깅용 출력

        cursor = DBConnect.get_db().cursor()
        sql_insert = 'INSERT INTO REVIEW (USER_ID, STORE_ID, CONTENTS, RATE, IMAGE) VALUES (%s, %s, %s, %s, %s)'
        ret_cnt = cursor.execute(sql_insert, (user_id, store_id, contents, rate, image))
        DBConnect.get_db().commit()

        store = StoreDAO.get_store_by_id(store_id)
        StoreDAO.update_store_rate(store['store_id'], ReviewDAO.get_rate(store_id))
        # todo: update sotre pk issue

        ret = ReviewDAO.get_reviews(store_id)
        return ret
        
    # 리뷰 업데이트
    @staticmethod
    def update_review(contents, rate, review_id, store_id, image=None):
        cursor = DBConnect.get_db().cursor()
        sql_update = 'UPDATE REVIEW SET CONTENTS=%s, RATE=%s, IMAGE=%s WHERE REVIEW_ID=%s'
        ret_cnt = cursor.execute(sql_update, (contents, rate, image, review_id))
        DBConnect.get_db().close()
        ret = ReviewDAO.get_reviews(store_id)
        return ret
    
    # 리뷰 삭제
    @staticmethod
    def delete_review(review_id, store_id):
        cursor = DBConnect.get_db().cursor()
        sql_delete = 'DELETE FROM REVIEW WHERE REVIEW_ID=%s'
        ret_cnt = cursor.execute(sql_delete, (review_id))
        DBConnect.get_db().close()
        ret = ReviewDAO.get_reviews(store_id)
        return ret