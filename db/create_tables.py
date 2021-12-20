

import psycopg2
from config import config
from db_obj.db import DataBase


def db_version():
    """  """

    conn = DataBase()
    conn.test_conn()


def create_tables():
    """  """

    commands = (
        """
        CREATE TABLE troops (
            id serial, -- Идентификатор рода войск
            title  varchar NOT NULL, -- имя тип рода войск
            url varchar NOT NULL, -- URL адресс рода войск
            PRIMARY KEY ( id ),
            UNIQUE ( title ),
            UNIQUE ( url )

        )
        """
        ,
        """
        CREATE TABLE veterans(
            id serial, -- Идентификатор таблицы ветераны
            troops_id int NOT NULL, --  id типа войск
            name varchar NOT NULL, -- имена ветеранов
            url varchar NOT NULL, -- url адресс хранения воспоминания
            text text, -- текст воспоминания
            PRIMARY KEY ( id ),
            UNIQUE ( url ),
            FOREIGN KEY ( troops_id )
                REFERENCES troops ( id )
                ON DELETE RESTRICT
        )
        """
      
    )

    conn = DataBase()
    conn.create_table(commands)

def create_tables_one():
    """  """
    
    commands = (
        """
        CREATE TABLE search_phrase(
            id serial,  --Идентификатор таблицы phrase
            phrase varchar NOT NULL, -- Поисковая фраза
            is_homonym boolean, -- Является ли слово омонимом
            PRIMARY KEY ( id ),
            UNIQUE ( phrase )
        )
        """
        ,
        """
        CREATE TABLE search(
            id_phrase int, -- Идентификатор таблицы phrase
            id_veterans int, -- Идентификатор таблицы veterans
            phrase_found varchar NOT NULL, -- Поисковое слово присутствует в тексте
            CHECK( phrase_found IN ( 'yes', 'not_verified', 'no' )),
            PRIMARY KEY ( id_phrase, id_veterans ),
            FOREIGN KEY ( id_veterans )
                REFERENCES veterans ( id ),
            FOREIGN KEY ( id_phrase )
                REFERENCES search_phrase ( id )
                ON DELETE CASCADE
        )
        """
    )

    conn = DataBase()
    conn.create_table(commands)


if __name__ == "__main__":
    # db_version()
    # create_tables()
    create_tables_one()

