


import psycopg2
from config import config


class DataBase:
    
    params = config()

    def __init__(self,):
        self.conn = psycopg2.connect(**self.params)
        self.cur = self.conn.cursor()

    def test_conn(self):
        """  """
        sql = ''' SELECT*FROM version() '''
        try:
            self.cur.execute(sql)
            res = self.cur.fetchone()
            print(res)
            self.cur.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
    
    def create_table(self, commands):
        """ """

        try:
            for command in commands:
                self.cur.execute(command)
            self.cur.close()
            self.conn.commit()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
