import psycopg2
from config import config


class DbParser:
    params = config()

    def __init__(self):
        self.conn = psycopg2.connect(**self.params)
        self.cur = self.conn.cursor()

    def insert_table_troops(self, data_parent):

        sql = """ INSERT INTO troops(title, url) VALUES(%s, %s) ON CONFLICT DO NOTHING; """
        try:
            self.cur.executemany(sql, data_parent)
            self.conn.commit()
            self.cur.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
    
    def select_id_troops(self, url_child):
        """   """
        sql = '''SELECT id FROM troops where url = %s; ''' 
        try:
            self.cur.execute(sql, (url_child,))
            res = self.cur.fetchone()[0]
            self.cur.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
        return res

    def insert_table_veterans(self, db_data_child):

        sql = """ INSERT INTO veterans(troops_id, name, url) VALUES(%s, %s, %s) ON CONFLICT DO NOTHING; """
        try:
            self.cur.executemany(sql, db_data_child)
            self.conn.commit()
            self.cur.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()

    def select_data_veterans(self):
        """  """
        sql = ''' SELECT id, url FROM veterans '''
        try:
            self.cur.execute(sql)
            res = self.cur.fetchall()
            self.cur.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
        return res

    def update_table_veterans(self, data_grandchild):
        """  """
        sql = """ UPDATE veterans SET text = %s WHERE url = %s """
        try:
            self.cur.executemany(sql, data_grandchild)
            self.conn.commit()
            self.cur.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
