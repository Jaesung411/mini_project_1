import pymysql

class DBConnect:
    @classmethod
    def get_db(cls):
        return pymysql.connect(
            host='127.0.0.1',
            user='user1',
            passwd='qwer1234',
            db='proj',
            charset='utf8',
            autocommit=True
        )

class ImageDAO:
    # select
    def get_images(self):
        ret = []
        cursor = DBConnect.get_db().cursor()
        sql_select = 'SELECT * FROM image'
        try:
            cursor.execute(sql_select)
            rows = cursor.fetchall()
            for row in rows:
                temp = {
                    'image_id': row[0],
                    'store_id': row[1],
                    'path': row[2]                 
                }
                ret.append(temp)
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            cursor.close()
        return ret

    def get_images_by_store_id(self, store_id):
        ret = []
        cursor = DBConnect.get_db().cursor()
        sql_select = 'SELECT image_id, path FROM image WHERE store_id=%s'
        cursor.execute(sql_select, (store_id,))
        rows = cursor.fetchall()
        for row in rows:
            ret.append({
                'image_id': row[0],
                'path': row[1]
            })
        cursor.close()
        return ret

    def insert_image(self, store_id, path):
        connection = DBConnect.get_db()
        cursor = connection.cursor()
        query = "INSERT INTO image (store_id, path) VALUES (%s, %s)"
        cursor.execute(query, (store_id, path))
        connection.commit()
        cursor.close()
        connection.close()

    def update_image(self, image_id, store_id, path):
        connection = DBConnect.get_db()
        cursor = connection.cursor()
        sql_update = 'UPDATE image SET store_id=%s, path=%s WHERE image_id=%s'
        ret_cnt = cursor.execute(sql_update, (store_id, path, image_id))
        connection.commit()
        cursor.close()
        connection.close()
        return f'update OK : {ret_cnt}'

    def delete_image(self, image_id):
        connection = DBConnect.get_db()
        cursor = connection.cursor()
        sql_delete = 'DELETE FROM image WHERE image_id=%s'
        ret_cnt = cursor.execute(sql_delete, (image_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return f'delete OK : {ret_cnt}'

    def get_max_image_id(self):
        connection = DBConnect.get_db()
        cursor = connection.cursor()
        sql_select = 'SELECT MAX(image_id) FROM image'
        cursor.execute(sql_select)
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result and result[0] is not None else 0
    
    

if __name__ == '__main__':
    image_list = ImageDAO().get_images()
    print(image_list)