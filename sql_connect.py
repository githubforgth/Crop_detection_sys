import pymysql
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)


class SQLConnector:
    def __init__(self, host, user, password, database):
        self.db = pymysql.connect(host=host, user=user, password=password, database=database,
                                  cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.db.cursor()

    def execute_query(self, sql, values=None):
        try:
            logging.info(f"Executing SQL: {sql} with values {values}")
            if values:
                self.cursor.execute(sql, values)
            else:
                self.cursor.execute(sql)
            self.db.commit()
            return self.cursor.fetchall()  # Return results for select queries
        except pymysql.MySQLError as e:
            self.db.rollback()
            logging.error(f"Error executing query: {e}")
            return None

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

    def get_all_users(self):
        query = "SELECT * FROM crop"
        return self.execute_query(query)

    def add_advice(self, disease_name, advice_content):
        query = "INSERT INTO advice (title, content) VALUES (%s, %s)"
        data = (disease_name, advice_content)
        return self.execute_query(query, data)

    def sql_select(self, table, columns='*', where=None):
        if not columns:
            columns = '*'

        sql_where = ''
        values = None
        if where:
            sql_where = "WHERE " + ' AND '.join([f"{key} = %s" for key in where.keys()])
            values = list(where.values())

        sql = f"SELECT {columns} FROM {table} {sql_where}"
        logging.info(f"SQL Query: {sql} with values: {values}")  # 添加日志
        return self.execute_query(sql, values)

    def sql_delete(self, table, where):
        if not where:
            logging.error("Error where clause!")
            return

        sql_where = "WHERE " + ' AND '.join([f"{key} = %s" for key in where.keys()])
        sql = f"DELETE FROM {table} {sql_where}"
        self.execute_query(sql, list(where.values()))

    def search_advices(self, query, page, per_page):
        offset = (page - 1) * per_page
        like_query = f"%{query}%"

        advices = self.execute_query(
            "SELECT * FROM advice WHERE title LIKE %s LIMIT %s OFFSET %s",
            (like_query, per_page, offset)
        )
        total = self.execute_query(
            "SELECT COUNT(*) AS total FROM advice WHERE title LIKE %s",
            (like_query,)
        )[0]['total']

        return advices, total

    def __del__(self):
        self.cursor.close()
        self.db.close()
