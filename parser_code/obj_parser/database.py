import psycopg2
from parser_code.config import config

params = config()


class DatabaseParser:
    params = config()

    def __init__(self):
        self.conn = psycopg2.connect(**self.params)
        self.cur = self.conn.cursor()

    def insert_table_troops(self, data_parent):

        sql = """ INSERT INTO troops(type_name, url) VALUES(%s, %s) ON CONFLICT DO NOTHING; """
        try:
            self.cur.executemany(sql, data_parent)
            self.conn.commit()
            self.cur.close()
            print('You saved the data in the table: troops')
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()

    def select_table_troops(self):

        sql = """ SELECT troops_id, url FROM troops; """
        try:
            self.cur.execute(sql)
            data = self.cur.fetchall()
            self.cur.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()

        return data

    def insert_table_veterans(self, data_lm_page):

        sql = """ INSERT INTO veterans(troops_id, names_veterans, url_memories) VALUES(%s, %s, %s) ON CONFLICT DO NOTHING; """
        try:
            self.cur.executemany(sql, data_lm_page)
            self.conn.commit()
            self.cur.close()
            print('Данные внесены в таблицу veterans, атрибуты (troops_id, names_veterans, url_memories)')
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()

    def insert_table_veterans_one(self, data_grandchildren):

        sql = """ UPDATE veterans SET memories = %s WHERE url_memories = %s; """
        try:
            self.cur.executemany(sql, data_grandchildren)
            self.conn.commit()
            self.cur.close()
            print('Данные внесены в таблицу veterans, атрибут memories')
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()