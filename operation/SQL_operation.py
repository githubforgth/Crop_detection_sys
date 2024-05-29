#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2024/2/19 下午9:01
# @Author : Gao_Taiheng
# @File : SQL_operation.py
import pymysql
import os


# ['username', 'email', 'userid', 'phonenumber', 'password', 'user_class', 'history']
class MySQLHelper:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = os.environ.get("SQL_USER")
        self.password = os.environ.get("SQL_PASSWORD")
        self.database = database
        self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                          database=self.database)
        self.cursor = self.connection.cursor()

    def execute_query(self, query, data=None):
        try:
            self.cursor.execute(query, data)
            return self.cursor.fetchall()
        except pymysql.Error as e:
            print(f"Error executing query: {e}")
            return None

    def execute_update(self, query, data=None):
        try:
            self.cursor.execute(query, data)
            self.connection.commit()
            return True
        except pymysql.Error as e:
            print(f"Error updating data: {e}")
            self.connection.rollback()
            return False

    def close_connection(self):
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    helper = MySQLHelper(host='localhost', user='root', password='123456', database='crop')

    # 示例用法
    # 查询数据
    results = helper.execute_query("SELECT * FROM your_table")
    print(results)

    # 更新数据
    update_query = "UPDATE your_table SET column1 = %s WHERE id = %s"
    update_data = ("new_value", 1)
    if helper.execute_update(update_query, update_data):
        print("Data updated successfully")

    # 关闭连接
    helper.close_connection()
