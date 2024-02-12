#!/usr/bin/env pythonphone
# -- coding: utf-8 --
# @Time : 2024/1/14 下午7:39
# @Author : Gao_Taiheng
# @File : sql_connect.py
import pymysql

db = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='crop')
cursor = db.cursor()
# ['username', 'email', 'userid', 'phonenumber', 'password', 'user_class', 'history']


def sql_update(table, data: dict, where: dict = None):
    if where is None:
        sql_where = ""
    else:
        sql_where = "WHERE " + ' AND '.join([f"{key} = '{val}'" for key, val in where.items()])

    set_clause = ', '.join([f"{key} = '{val}'" for key, val in data.items()])
    sql = f"UPDATE {table} SET {set_clause} {sql_where}"

    cursor.execute(sql)
    db.commit()


def sql_insert(table, data):
    if not data:
        raise ValueError("Error data!")

    columns = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    sql = f'INSERT INTO {table} ({columns}) VALUES ({values})'
    print(sql, list(data.values()))

    # Use parameterized query to prevent SQL injection
    cursor.execute(sql, list(data.values()))
    db.commit()


def sql_select(table, columns=None, where=None):
    if columns is None:
        columns = '*'

    sql_where = ''
    if where:
        sql_where = "WHERE " + ' AND '.join([f"{key} = '{val}'" for key, val in where.items()])
        print(sql_where)
    sql = f"SELECT {columns} FROM {table} {sql_where}"
    cursor.execute(sql)
    # 获取所有查询结果
    results = cursor.fetchall()
    return results


def sql_delete(table, where):
    if not where:
        raise ValueError("Error where clause!")

    sql_where = "WHERE " + ' AND '.join([f"{key} = '{val}'" for key, val in where.items()])
    sql = f"DELETE FROM {table} {sql_where}"

    cursor.execute(sql)
    db.commit()


if __name__ == "__main__":
    pass
