#!/usr/bin/env pythonphone
# -- coding: utf-8 --
# @Time : 2024/1/14 下午7:39
# @Author : Gao_Taiheng
# @File : sql_connect.py
import pymysql
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)


class SQLConnector:
    def __init__(self, host, user, password, database):
        self.db = pymysql.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.db.cursor()

    def execute_query(self, sql, values=None):
        try:
            if values:
                self.cursor.execute(sql, values)
            else:
                self.cursor.execute(sql)
            self.db.commit()
        except pymysql.MySQLError as e:
            self.db.rollback()
            logging.error(f"Error executing query: {e}")

    def sql_update(self, table, data, where=None):
        if where:
            sql_where = "WHERE " + ' AND '.join([f"{key} = %s" for key in where.keys()])
            values = list(data.values()) + list(where.values())
        else:
            sql_where = ""
            values = list(data.values())

        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} {sql_where}"
        self.execute_query(sql, values)

    def sql_insert(self, table, data):
        if not data:
            logging.error("Error data!")
            return

        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = f'INSERT INTO {table} ({columns}) VALUES ({values})'
        self.execute_query(sql, list(data.values()))

    def sql_select(self, table, columns=None, where=None):
        if not columns:
            columns = '*'

        sql_where = ''
        values = None
        if where:
            sql_where = "WHERE " + ' AND '.join([f"{key} = %s" for key in where.keys()])
            values = list(where.values())

        sql = f"SELECT {columns} FROM {table} {sql_where}"
        self.cursor.execute(sql, values)
        results = self.cursor.fetchall()
        return results

    def sql_delete(self, table, where):
        if not where:
            logging.error("Error where clause!")
            return

        sql_where = "WHERE " + ' AND '.join([f"{key} = %s" for key in where.keys()])
        sql = f"DELETE FROM {table} {sql_where}"
        self.execute_query(sql, list(where.values()))

    def __del__(self):
        self.cursor.close()
        self.db.close()


if __name__ == "__main__":
    # Usage example
    sql_connector = SQLConnector(host='localhost', user='root', password='123456', database='crop')

    # Insert example
    data_insert = {'username': 'test', 'email': 'test@example.com', 'password': 'test123', 'phonenumber': 123456}
    sql_connector.sql_insert('crop', data_insert)

    # Update example
    data_update = {'email': 'newemail@example.com'}
    where_update = {'username': 'test'}
    sql_connector.sql_update('crop', data_update, where_update)

    # Select example
    results = sql_connector.sql_select('crop', where={'username': 'test'})
    print(results)

    # Delete example
    where_delete = {'username': 'test'}
    sql_connector.sql_delete('crop', where_delete)
