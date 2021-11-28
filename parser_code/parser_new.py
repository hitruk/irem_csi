

# from obj_parser.database import DatabaseParser
from obj_parser.pages import HttpQuery, ElementPageParent, ElementPageChild, ElementPageGrandchildren
import os
import re

def query_parent_page(BASE_URL):
    """ Get parent html page """
    
    query = HttpQuery(BASE_URL, params=None)
    html = query.get_page_html()
    return html

def save_parent_html(html):
    """ Save parent html page """

    with open('parent_page.html', 'w') as file:
        file.write(html)

def open_parent_html():
    """ Open parent html page """

    with open('parent_page.html', 'r') as file:
        html = file.read()
    return html

def element_parent_page(html):
    """ Get the elements the parent page and store """
    
    elements = ElementPageParent(html)
    data_parent = elements.get_parent_element()
    return data_parent

def save_data_parent(data_parent):
    """ Save the data parent page in the database """

    db = DatabaseParser()
    db.insert_table_troops()
    print('Data parent page saved in the database table: [(troops.type_name, troops.url)]')

def get_url_child(BASE_URL, data_parent):
    """ Get url child from list urls child """

    # в дальнейшем использовать цикл, чтобы получить каждый url_child из списка
    # for row in data_parent:
    #     
    url_child = BASE_URL + data_parent[0][1]
    print(url_child)
    return url_child

def count_child(url_child):
    """ Get the number of dynamically loaded pages """

    query = HttpQuery(url_child, params=None)
    html = query.get_page_html()
    elements = ElementPageChild(html)
    count_page = elements.count_page()  # количество динамически подгружаемых страниц
    return count_page

def query_child_page(url_child, count_page):
    """ Get child html page and page elements """
    
    params = {'page': int(count_page)}
    query = HttpQuery(url_child, params)
    html_child = query.get_page_html()
     
    return html_child

def save_html_child(html_child, url_child):
    """ Save child html page """
    
    pattern = r"([a-z]+)\/$"
    name = (re.findall(pattern, url_child)[0])
    print(name)
    with open(name+'.html', 'w') as file:
        file.write(html_child)

def element_child_page(html_child):
    """ Get the elements a child page """

    elements = ElementPageChild(html_child)
    data_child = elements.get_child_element()
    print(data_child[0])
    return data_child[0]

def query_grandchild_page(BASE_URL, data_child):
    """ Get grandchild html page and elements """

    url_grandchild = BASE_URL + data_child[1]
    query = HttpQuery(url_grandchild, params=None)
    html = query.get_page_html()
    elements = ElementPageGrandchildren(html)
    text = elements.get_grandchildren_element()
    print(text)

# old_code
def data_parent_page(BASE_URL):
    """ Get parent page data """

    query = HttpQuery(BASE_URL, params=None)
    html = query.get_page_html()

    elements = ElementPageParent(html)
    data_page_parent = elements.get_parent_element()  # [(title, url)]
    
    db = DatabaseParser()
    db.insert_table_troops(data_page_parent)
    print('function executed: save_data_parent()')
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
    
    # new code
    BASE_URL = 'https://iremember.ru'   

    if os.path.exists('parent_page.html'):
        pass
    else:
        html = query_parent_page(BASE_URL)
        save_parent_html(html)
    
    html_parent = open_parent_html()
    data_parent = element_parent_page(html_parent)
    # save_data_parent(data_parent)
    url_child = get_url_child(BASE_URL, data_parent)
    count_child = count_child(url_child)
    html_child = query_child_page(url_child, count_child)
    save_html_child(html_child, url_child)
    element_child_page(html_child)
    

    #query_grandchild_page(BASE_URL, data_child)


    # old_code
    ''' BASE_URL = 'https://iremember.ru'

    data_parent_page(BASE_URL)
    for row in extract_data_troops():
        id_troops = row[0]
        url = BASE_URL + row[1]
        print('!')
        print(url)
        data_child_page(url, id_troops, BASE_URL)'''
