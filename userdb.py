import pymysql

class UserDBConnect:
    @classmethod
    def get_db(self):
        return pymysql.connect(
            host='127.0.0.1',
            user='userdb',
            passwd='qwer1234',
            db='mini_proj',
            charset='utf8',
            autocommit=True
        )
        
# DAO : DATA ACCESS OBJECT
# 기능 클래스로 사용
class userDAO :
    # select
    def get_users(self):
        cursor = UserDBConnect.get_db().cursor()
        sql = 'SELECT * FROM login'
        cursor.execute(sql)
        result = cursor.fetchall()
        UserDBConnect.get_db().close()
        return result
    
    # 사용자 인증
    def authenicate(self, useremail, password):
        cursor = UserDBConnect.get_db().cursor()
        sql = 'SELECT * FROM login WHERE email=%s AND passwd=%s'
        UserDBConnect.get_db().close()
        cursor.execute(sql,(useremail,password))
        user = cursor.fetchone()
        if password == user[2]:
            return user
        return None
    
    # 회원 가입
    def create_user(self, email, passwd, nickname, name, auth):
        cursor = UserDBConnect.get_db().cursor()
        sql = 'INSERT INTO login ( email, passwd, name, nickname, role ) VALUES (%s,%s,%s,%s,%s)'
        ret_cnt = cursor.execute(sql,(email, passwd, name, nickname,auth))
        UserDBConnect.get_db().close()
        return ret_cnt
        
    # 회원 정보 수정
    def update_user(self, userno, email, passwd, nickname, name):
        cursor = UserDBConnect.get_db().cursor()
        sql = 'UPDATE login SET email=%s, passwd=%s, nickname=%s, name=%s WHERE userno=%s'
        ret_cnt = cursor.execute(sql,( email, passwd, nickname, name, userno))
        UserDBConnect.get_db().close()
    
    # 회원 탈퇴
    def delete_user(self, userno):
        cursor = UserDBConnect.get_db().cursor()
        sql = 'DELETE FROM login WHERE userno=%s'
        ret_cnt = cursor.execute(sql,(userno))
        UserDBConnect.get_db().close()
        
# if __name__=='__main__':
#     print(UserDBConnect.get_db())
#     print(userDAO().create_user('root@root.com', '1234', 'root', 'root','0'))
    # print(userDAO().delete_user('1237'))
    # print(userDAO().update_user('1','root@root.com', '1234', 'root', 'root','0'))