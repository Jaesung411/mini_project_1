import pymysql

class DBConnect:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def get_db(self):
        return pymysql.connect(
            host='127.0.0.1',
            user='',
            passwd='',
            db='',
            charset='utf8',
            autocommit=True
        )

class ReviewDAO:
    #seelct
    def get_reviews(self, store_id):
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
    def insert_review(self, user_id, store_id, contents, rate, image):
        cursor = DBConnect.get_db().cursor()
        sql_insert = 'INSERT INTO REVIEW (USER_ID, STORE_ID, CONTENTS, RATE, IMAGE) values (%s, %s, %s, %s)'
        ret_cnt = cursor.execute(sql_insert, (menu_id, store_id, menu_name, price))
        DBConnect.get_db().close()
        return f'INSERT OK : {ret_cnt}'
    
    # update
    def update_review(self, user_id, store_id, contents, rate, image):
        cursor = DBConnect.get_db().cursor()
        sql_update = 'UPDATE REVIEW SET USER_ID=%s, STORE_ID=%s, CONTENTS=%s, RATE=%s, IMAGE=%s'
        ret_cnt = cursor.execute(sql_update, (menu_id, store_id, menu_name, price))
        DBConnect.get_db().close()
        return f'UPDATE OK : {ret_cnt}'
    
    # delete
    def delete_review(self, review_id):
        cursor = DBConnect.get_db().cursor()
        sql_delete = 'DELETE FROM REVIEW WHERE REVIEW_ID=%s'
        ret_cnt = cursor.execute(sql_delete, (menu_id))
        DBConnect.get_db().close()
        return f'DELETE OK : {ret_cnt}'