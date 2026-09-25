import mysql.connector
from mysql.connector import errorcode
from models import User

HOST = "localhost"
USER = "root"
PASSWORD = "password"
DATABASE = "app"


db = mysql.connector.connect(
    host=HOST,
    port=3306,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)


class DbWrapper:
    @staticmethod
    def does_user_exist(user: User) -> bool:
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE user = %s", (user.user,))
        return bool(cur.fetchone())


    @staticmethod
    def add_user(user: User) -> bool:
        cur = db.cursor()
        try:
            cur.execute("INSERT INTO users(user, password) VALUES (%s, %s)", (user.user, user.password))
        except mysql.connector.IntegrityError as e:
            if e.errno == errorcode.ER_DUP_ENTRY:
                return False
            raise e
        db.commit()
        return True
