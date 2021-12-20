

from product_code.db_obj.database import Database
from psycopg2 import DatabaseError


def drop_tables():

    conn = None

    try:
        conn = Database()
        conn.drop_all_tables()
        conn.conn_commit()
        conn.cur_close()
    except(Exception, DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.conn_close()

drop_tables()
