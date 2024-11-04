import pymysql

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
    #seelct
    @staticmethod
    def get_reviews(store_id):
        ret = []
        cursor = DBConnect.get_db().cursor()

        sql_select = 'SELECT REVIEW_ID, CONTENTS, RATE, IMAGE FROM REVIEW WHERE STORE_ID = %s'
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
    
    # insert
    @staticmethod
    def insert_review(user_id, store_id, contents, rate, image=None):
        print(f'store_id: {store_id}')  # 디버깅용 출력

        cursor = DBConnect.get_db().cursor()
        sql_insert = 'INSERT INTO REVIEW (USER_ID, STORE_ID, CONTENTS, RATE, IMAGE) VALUES (%s, %s, %s, %s, %s)'
        ret_cnt = cursor.execute(sql_insert, (user_id, store_id, contents, rate, image))
        DBConnect.get_db().commit()
        ret = ReviewDAO.get_reviews(store_id)
        return ret
        
    # update
    @staticmethod
    def update_review(contents, rate, review_id, store_id, image=None):
        cursor = DBConnect.get_db().cursor()
        sql_update = 'UPDATE REVIEW SET CONTENTS=%s, RATE=%s, IMAGE=%s WHERE REVIEW_ID=%s'
        ret_cnt = cursor.execute(sql_update, (contents, rate, image, review_id))
        DBConnect.get_db().close()
        ret = ReviewDAO.get_reviews(store_id)
        return ret
    
    # delete
    @staticmethod
    def delete_review(review_id, store_id):
        cursor = DBConnect.get_db().cursor()
        sql_delete = 'DELETE FROM REVIEW WHERE REVIEW_ID=%s'
        ret_cnt = cursor.execute(sql_delete, (review_id))
        DBConnect.get_db().close()
        ret = ReviewDAO.get_reviews(store_id)
        return ret