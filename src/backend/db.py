import mysql.connector
from random import choices as rand_choices
from string import printable as str_printable
from mysql.connector import errorcode
from models import Token, User, UserCredential

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


    @staticmethod
    def _gen_token() -> str:
        TOKEN_LENGTH = 150
        token = ''.join(rand_choices(str_printable, k=TOKEN_LENGTH))
        while DbWrapper.get_token(token):
            token = ''.join(rand_choices(str_printable, k=TOKEN_LENGTH))
        return token


    @staticmethod
    def get_token(token: str) -> Token | None:
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT user_id, token, (expires_at < NOW()) AS expired FROM cookies WHERE token = %s", (token,))

        token_row = cur.fetchone()
        if token_row is None:
            return None
        return Token(**token_row)

    @classmethod
    def get_user_by_token(cls, token: Token) -> User:
        return cls.get_user_by_id(token.user_id)


    @staticmethod
    def get_user_by_id(id: int) -> User | None:
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE id = %s", (id,))

        user_data = cur.fetchone()
        if user_data is None:
            return None
        return User.model_validate(user_data)


    @classmethod
    def create_new_cookies(cls, user: User) -> str:
        token: str = cls._gen_token()
        cur = db.cursor()

        cur.execute(
            """
            INSERT INTO cookies(user_id, token, expires_at)
            VALUES (%s, %s , DATE_ADD(NOW(), INTERVAL 7 DAY))
            """,
            (user.id, token),
        )
        db.commit()
        return token


    @staticmethod
    def get_user_by_username(username: str) -> User | None:
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE user = %s", (username,))
        user_data = cur.fetchone()
        if user_data is None:
            return None
        return User.model_validate(user_data)

    @staticmethod
    def _password_match(plain_password: str, hashed_password: str) -> bool:
        return plain_password == hashed_password

    @classmethod
    def verify_credential(cls, cred: UserCredential) -> User | None:
        user = cls.get_user_by_username(cred.user)
        if user is None or not cls._password_match(cred.password, user.password):
            return None
        return user
