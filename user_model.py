from flask_login import UserMixin
from sql_connect import SQLConnector


class User(UserMixin):
    def __init__(self, id, username, phone, password):
        self.id = id
        self.username = username
        self.phone = phone
        self.password = password  # Store hashed password

    @staticmethod
    def get(user_id):
        helper = SQLConnector(host='localhost', user='root', password='123456', database='crop')
        user_data = helper.sql_select('crop', where={'userid': user_id})
        if user_data:
            user_info = user_data[0]
            return User(id=user_info['userid'], username=user_info['username'], phone=user_info['phonenumber'],
                        password=user_info['password'])
        return None

    @staticmethod
    def get_by_phone(phone):
        helper = SQLConnector(host='localhost', user='root', password='123456', database='crop')
        user_data = helper.sql_select('crop', where={'phonenumber': phone})
        if user_data:
            user_info = user_data[0]
            return User(id=user_info['userid'], username=user_info['username'], phone=user_info['phonenumber'],
                        password=user_info['password'])
        return None
