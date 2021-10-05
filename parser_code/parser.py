

from obj_parser.database import DatabaseParser
from obj_parser.pages import HttpQuery, ElementPageParent, ElementPageChild, ElementPageGrandchildren


def data_parent_page(BASE_URL):
    """ Get parent page data """

    query = HttpQuery(BASE_URL, params=None)
    html = query.get_page_html()

    elements = ElementPageParent(html)
    data_page_parent = elements.get_parent_element()  # [(title, url)]
    db = DatabaseParser()
    db.insert_table_troops(data_page_parent)
    print('---function executed: save_data_parent()---')
    return data_page_parent


def extract_data_troops():
    """ SELECT troops_id, url FROM troops """

    db = DatabaseParser()
    data_table_troops = db.select_table_troops()  # Данные таблицы troops: troops_id, url
    print(data_table_troops)
    for row in data_table_troops:
        yield row  # [(troops_id, url)]


def data_child_page(url, id_troops, BASE_URL):
    """ Get child page data """

    # страницы подгружаются пролистыванием
    # количество подгружаемых страниц неизвестно
    # получаем все подгружаемые страницы
    n = 1  # номерация начинается с 1
    one = []  # список, необходимый для сравнения
    # блок для получения всех страниц, добавляющихся пролистыванием, скрол
    while True:
        params = {'page': n}
        query = HttpQuery(url, params)
        html = query.get_page_html()
        if html == None:
            break
        elements = ElementPageChild(html)
        # (id_troops, title, url), для вставки в таблицу veterans
        data_child = elements.get_child_element(id_troops)
        if one[:-1] != data_child[:-1]:  # !!!! [:-1]
            one = data_child
        else:
            break
        n += 1
    print(len(data_child))  # data_child: (id_troops, title, url)

    db = DatabaseParser()
    db.insert_table_veterans(data_child)

    data_grandchildren = []
    m = 1
    for row in data_child:
        # print(row[0])  # id_troops
        # print(row[1])  # title
        # print(row[2])  # url
        url_grandchild = BASE_URL + row[2]
        print(m, url_grandchild)
        # --- get grandchild page data ---
        query = HttpQuery(url_grandchild, params=None)
        html = query.get_page_html()
        elements = ElementPageGrandchildren(html)
        text = elements.get_grandchildren_element()
        data_grandchildren.append((text, row[2]))  # (text, url), url - grandchild page
        m += 1
    print(len(data_grandchildren))
    db = DatabaseParser()
    db.insert_table_veterans_one(data_grandchildren)


if __name__ == "__main__":

    BASE_URL = 'https://iremember.ru'

    data_parent_page(BASE_URL)
    for row in extract_data_troops():
        id_troops = row[0]
        url = BASE_URL + row[1]
        print('!')
        print(url)
        data_child_page(url, id_troops, BASE_URL)
