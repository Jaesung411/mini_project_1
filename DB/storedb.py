import pymysql

class DBConnect:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def get_db(self):
        """DB 연결을 반환하는 메서드"""
        return pymysql.connect(
            host='127.0.0.1',
            user='user1',
            passwd='qwer1234',
            db='mini_proj',
            charset='utf8',
            autocommit=True
        )

class StoreDAO:
    def get_stores(self):
        """모든 가게 정보를 조회하여 반환"""
        ret = []
        try:
            with DBConnect.get_db().cursor() as cursor:
                sql_select = 'SELECT * FROM store'
                cursor.execute(sql_select)
                rows = cursor.fetchall()
                for row in rows:
                    temp = {
                        'store_id': row[0],
                        'name': row[1],
                        'address': row[2],
                        'image': row[3],
                        'rate': row[4],
                        'food_type': row[5]
                    }
                    ret.append(temp)
        except Exception as e:
            print(f"Error: {e}")
        return ret
    
    def get_store_by_name(self, name):
        """가게 이름으로 검색하여 해당 가게 정보를 반환"""
        cursor = DBConnect.get_db().cursor()
        sql_select = 'SELECT * FROM store WHERE name=%s'
        cursor.execute(sql_select, (name,))
        row = cursor.fetchone()  # 단일 행 가져오기
        DBConnect.get_db().close()
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
    
    def get_store_by_id(self, store_id):
        """가게 ID로 검색하여 해당 가게 정보를 반환"""
        cursor = DBConnect.get_db().cursor()
        sql_select = 'SELECT * FROM store WHERE store_id = %s'
        cursor.execute(sql_select, (store_id,))
        row = cursor.fetchone()
        DBConnect.get_db().close()
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
    
    def insert_store(self, store_id, name, address, image_path, rate, food_type):
        """새로운 가게를 추가"""
        cursor = DBConnect.get_db().cursor()
        
        # SQL 쿼리: image_path는 파일 경로로 저장
        sql_insert = '''
        INSERT INTO store (store_id, name, address, image, rate, food_type)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        
        try:
            # 데이터 삽입을 위해 전달된 파라미터들을 실행
            ret_cnt = cursor.execute(sql_insert, (store_id, name, address, image_path, rate, food_type))
            print(f"SQL Insert executed. Rows affected: {ret_cnt}")
            
            # DB에 변경 사항을 커밋
            DBConnect.get_db().commit()  
        except Exception as e:
            # 예외 발생 시 롤백
            print(f"Error executing insert: {e}")
            DBConnect.get_db().rollback()  
        finally:
            # DB 연결 닫기
            DBConnect.get_db().close()
        
        # 삽입 성공 메시지 반환
        return f'insert OK : {ret_cnt}'
    
    def update_store(self, store_id, name, address, image, rate, food_type):
        """기존 가게의 정보를 수정"""
        cursor = DBConnect.get_db().cursor()
        sql_update = '''UPDATE store
                        SET name=%s, address=%s, image=%s, rate=%s, food_type=%s
                        WHERE store_id=%s'''
        try:
            ret_cnt = cursor.execute(sql_update, (name, address, image, rate, food_type, store_id))
            DBConnect.get_db().commit()  # 데이터베이스 변경사항 커밋
            return f'update OK : {ret_cnt}'
        except Exception as e:
            print(f"Error: {e}")
            DBConnect.get_db().rollback()  # 오류 시 롤백
            return f'Error updating store: {e}'
    
    def delete_store(self, store_id):
        """가게 정보를 삭제"""
        cursor = DBConnect.get_db().cursor()
        sql_delete = 'DELETE FROM store WHERE store_id=%s'
        try:
            ret_cnt = cursor.execute(sql_delete, (store_id,))
            DBConnect.get_db().commit()  # DB에 반영
            return f'delete OK : {ret_cnt}'
        except Exception as e:
            print(f"Error deleting store: {e}")
            DBConnect.get_db().rollback()  # 실패 시 롤백
        finally:
            DBConnect.get_db().close()
    
if __name__=='__main__':
    # print (DBConnect.get_db())
    # print (StoreDAO().insert_store(7, '버거킹', '서울시 강남구', '/images/xxx.jpg', '0.0', '패스트푸드'))
    # print (StoreDAO().update_store(7, '맥도날드', '서울시 강남구', '/images/xxx.jpg', '0.0', '패스트푸드'))
    # print (StoreDAO().delete_store(7))
    
    store_list = StoreDAO().get_stores()
    print(store_list)
