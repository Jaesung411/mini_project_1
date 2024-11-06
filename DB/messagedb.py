from datetime import datetime
import pymysql

class DBConnect:
    @classmethod
    def get_db(self):
        return pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='qwer1234',
            db='mini_proj',
            charset='utf8',
            autocommit=True
        )

class MessageDAO:
    # select
    def get_messages(self):
        ret = []
        connection = None
        try:
            connection = DBConnect.get_db()
            cursor = connection.cursor()
            sql_select = 'SELECT * FROM message'
            cursor.execute(sql_select)
            rows = cursor.fetchall()
            for row in rows:
                temp = {
                    'message_id': row[0], 
                    'user_id': row[1], 
                    'name': row[2],
                    'contents': row[3]
                }
                ret.append(temp)
        except Exception as e:
            print("Error in get_messages:", e)
        finally:
            if connection:
                connection.close()
        return ret

    # insert
    def insert_message(self, user_id, name, contents, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now()  # Use current time if not provided
        connection = None
        try:
            connection = DBConnect.get_db()
            cursor = connection.cursor()
            sql_insert = 'INSERT INTO message (user_id, name, contents, timestamp) VALUES (%s, %s, %s, %s)'
            ret_cnt = cursor.execute(sql_insert, (user_id, name, contents, timestamp))
            return f'Insert OK : {ret_cnt}'
        except Exception as e:
            print("Error in insert_message:", e)
        finally:
            if connection:
                connection.close()

    # update
    def update_message(self, message_id, new_contents):
        connection = None
        try:
            connection = DBConnect.get_db()
            cursor = connection.cursor()
            sql_update = 'UPDATE message SET contents = %s WHERE message_id = %s'
            ret_cnt = cursor.execute(sql_update, (new_contents, message_id))
            return f'Update OK : {ret_cnt}'
        except Exception as e:
            print("Error in update_message:", e)
        finally:
            if connection:
                connection.close()

    # delete
    def delete_message(self, message_id):
        connection = None
        try:
            connection = DBConnect.get_db()
            cursor = connection.cursor()
            sql_delete = 'DELETE FROM message WHERE message_id = %s'
            ret_cnt = cursor.execute(sql_delete, (message_id,))
            return f'Delete OK : {ret_cnt}'
        except Exception as e:
            print("Error in delete_message:", e)
        finally:
            if connection:
                connection.close()