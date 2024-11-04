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
            db='proj',
            charset='utf8',
            autocommit=True
        )

class StoreDAO:
    # select
    def get_stores(self):
        ret = []
        cursor = DBConnect.get_db().cursor()
        sql_select = 'select * from store'
        try:
            cursor.execute(sql_select)
            rows = cursor.fetchall()
            for row in rows :
                temp = {
                    'store_id' : row[0],
                    'name' : row[1],
                    'address' : row[2],
                    'image' : row[3],
                    'rate' : row[4],
                    'food_type' : row[5]
                }
                ret.append(temp)
        except :
            pass
        finally :
            DBConnect.get_db().close()
        return ret
    
    # 가게 이름 불러오기
    def get_store_by_name(self, name):
        cursor = DBConnect.get_db().cursor()
        sql_select = 'SELECT * FROM store WHERE name=%s'
        cursor.execute(sql_select, (name,))
        row = cursor.fetchone()  # 단일 행 가져오기
        if row:
            return {
                'store_id': row[0],
                'name': row[1],
                'address': row[2],
                'image': row[3],
                'rate': row[4],
                'food_type': row[5]
            }
        return None
    
    # 가게 ID 불러오기
    def get_store_by_id(self, store_id):
        cursor = DBConnect.get_db().cursor()
        sql_select = 'SELECT * FROM store WHERE store_id = %s'
        cursor.execute(sql_select, (store_id,))
        row = cursor.fetchone()
        if row:
            return {
                'store_id': row[0],
                'name': row[1],
                'address': row[2],
                'image': row[3],
                'rate': row[4],
                'food_type': row[5]
            }
        return None  # 가게가 없으면 None 반환

    # insert
    def insert_store(self, store_id, name, address, image, rate, food_type):
        cursor = DBConnect.get_db().cursor()
        sql_insert = 'insert into store (store_id, name, food_type, address, image, rate) values (%s, %s, %s, %s, %s, %s)'
        ret_cnt = cursor.execute(sql_insert, (store_id, name, food_type, address, image, rate))
        DBConnect.get_db().close()
        return f'insert OK : {ret_cnt}'
    
    # update
    def update_store(self, store_id, name, address, image, rate, food_type):
        cursor = DBConnect.get_db().cursor()
        sql_update = 'update store set name=%s, food_type=%s, address=%s, image=%s, rate=%s where store_id=%s'
        ret_cnt = cursor.execute(sql_update, (name, food_type, address, image, rate, store_id))
        DBConnect.get_db().close()
        return f'update OK : {ret_cnt}'
    
    # delete
    def delete_store(self, store_id):
        cursor = DBConnect.get_db().cursor()
        sql_delete = 'delete from store where store_id=%s'
        ret_cnt = cursor.execute(sql_delete, (store_id))
        DBConnect.get_db().close()
        return f'delete OK : {ret_cnt}'
    
if __name__=='__main__':
    # print (DBConnect.get_db())
    # print (StoreDAO().insert_store(7, '버거킹', '서울시 강남구', '/images/xxx.jpg', '0.0', '패스트푸드'))
    # print (StoreDAO().update_store(7, '맥도날드', '서울시 강남구', '/images/xxx.jpg', '0.0', '패스트푸드'))
    # print (StoreDAO().delete_store(7))
    
    store_list = StoreDAO().get_stores()
    print(store_list)