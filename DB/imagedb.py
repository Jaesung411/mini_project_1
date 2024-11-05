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

class ImageDAO:
    # select
    def get_images(self):
        ret = []
        cursor = DBConnect.get_db().cursor()
        sql_select = 'select * from image'
        try:
            cursor.execute(sql_select)
            rows = cursor.fetchall()
            for row in rows :
                temp = {
                    'image_id' : row[0],
                    'store_id' : row[1],
                    'path' : row[2]                 
                }
                ret.append(temp)
        except :
            pass
        finally :
            DBConnect.get_db().close()
        return ret
    
    # 메뉴 이름, 가격 불러오기
    def get_menus_by_store_id(self, store_id):
        ret = []
        cursor = DBConnect.get_db().cursor()
        sql_select = 'SELECT menu_name, price FROM menu WHERE store_id = %s'
        cursor.execute(sql_select, (store_id,))
        rows = cursor.fetchall()
        DBConnect.get_db().close()
        for row in rows:
            ret.append({
                'menu_name': row[0],
                'price': row[1]
            })
        return ret
    
    # path 불러오기
    def get_images_by_store_id(self, store_id):
        ret = []
        cursor = DBConnect.get_db().cursor()
        sql_select = 'SELECT * FROM image WHERE store_id=%s'
        cursor.execute(sql_select, (store_id,))
        rows = cursor.fetchall()
        DBConnect.get_db().close()
        print(rows)
        for row in rows:
            ret.append({
                'image_id':row[0],
                'store_id':row[1],
                'path':row[2]
                })  # 경로만 리스트에 추가
        return ret
    
    # insert
    def insert_image(self, store_id, path):
        cursor = DBConnect.get_db().cursor()
        sql_insert = 'insert into image (store_id, path) values (%s, %s)'
        ret_cnt = cursor.execute(sql_insert, (store_id, path))
        DBConnect.get_db().close()
        return f'insert OK : {ret_cnt}'
    
    # update
    def update_image(self, image_id, store_id, path):
        cursor = DBConnect.get_db().cursor()
        sql_update = 'update image set image_id=%s, store_id=%s'
        ret_cnt = cursor.execute(sql_update, (image_id, store_id))
        DBConnect.get_db().close()
        return f'update OK : {ret_cnt}'
    
    # delete
    def delete_image(self, image_id):
        cursor = DBConnect.get_db().cursor()
        sql_delete = 'delete from image where image_id=%s'
        ret_cnt = cursor.execute(sql_delete, (image_id))
        DBConnect.get_db().close()
        return f'delete OK : {ret_cnt}'

    def get_max_image_id(self):
        connection = DBConnect.get_db()
        cursor = connection.cursor()
        sql_select = 'SELECT MAX(image_id) FROM image'
        cursor.execute(sql_select)
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result and result[0] is not None else 0
    