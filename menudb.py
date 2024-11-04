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

class MenuDAO:
    # select
    def get_menus(self):
        ret = []
        cursor = DBConnect.get_db().cursor()
        sql_select = 'select * from menu'
        try:
            cursor.execute(sql_select)
            rows = cursor.fetchall()
            for row in rows :
                temp = {
                    'menu_id' : row[0],
                    'store_id' : row[1],
                    'menu_name' : row[2],
                    'price' : row[3]                 
                }
                ret.append(temp)
        except :
            pass
        finally :
            DBConnect.get_db().close()
            
        return ret

    # insert
    def insert_menu(self, menu_id, store_id, menu_name, price):
        cursor = DBConnect.get_db().cursor()
        sql_insert = 'insert into menu (menu_id, store_id, menu_name, price) values (%s, %s, %s, %s)'
        ret_cnt = cursor.execute(sql_insert, (menu_id, store_id, menu_name, price))
        DBConnect.get_db().close()
        return f'insert OK : {ret_cnt}'
    
    # update
    def update_menu(self, menu_id, store_id, menu_name, price):
        cursor = DBConnect.get_db().cursor()
        sql_update = 'update store set menu_id=%s, store_id=%s, menu_name=%s, price=%s'
        ret_cnt = cursor.execute(sql_update, (menu_id, store_id, menu_name, price))
        DBConnect.get_db().close()
        return f'update OK : {ret_cnt}'
    
    # delete
    def delete_menu(self, menu_id):
        cursor = DBConnect.get_db().cursor()
        sql_delete = 'delete from menu where menu_id=%s'
        ret_cnt = cursor.execute(sql_delete, (menu_id))
        DBConnect.get_db().close()
        return f'delete OK : {ret_cnt}'
    
    def get_max_menu_id(self):
        cursor = DBConnect.get_db().cursor()
        sql_select = 'SELECT MAX(menu_id) FROM menu'
        cursor.execute(sql_select)
        result = cursor.fetchone()
        return result[0] if result and result[0] is not None else 0  # None 체크 추가
    
        # 가게 id 불러오기
    def get_menus_by_store_id(self, store_id):
        ret = []
        cursor = DBConnect.get_db().cursor()
        sql_select = 'SELECT menu_id, store_id, menu_name, price FROM menu WHERE store_id = %s'
        cursor.execute(sql_select, (store_id,))
        rows = cursor.fetchall()
        for row in rows:
            ret.append({
                'menu_id': row[0],
                'store_id': row[1],
                'menu_name': row[2],
                'price': row[3]
            })
        return ret
        
if __name__=='__main__':
    # print (DBConnect.get_db())
    # print (StoreDAO().insert_menu(22, '5', '고로아케', '10,000',))
    # print (StoreDAO().update_menu(22, '5', '타코야끼', '10,000',))
    # print (StoreDAO().delete_menu(22))
    
    menu_list = MenuDAO().get_menus()
    print(menu_list)