
from db_obj.db import DbParser
from obj_parser.pages import HttpQuery, ElementPageParent, ElementPageChild, ElementPageGrandchildren
import os
import re
from config import config

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
    print('Got elements parent page: (title, url)')
    return data_parent # [(title, url)]

def save_data_parent(data_parent):
    """ Save the data parent page in the database """

    db = DbParser()
    db.insert_table_troops(data_parent)
    print('Saved data parent page in database table: troops', '\n') 


# получаем дочерние страницы
def get_url_child(BASE_URL, data_parent):
    """ Get url child from list urls child """

    # в дальнейшем использовать цикл, чтобы получить каждый url_child из списка
    for row in data_parent:
        url_child = BASE_URL + row[1]
        print('Got url child page:', url_child)
        yield url_child

def count_child(url_child):
    """ Get the number of dynamically loaded pages """

    query = HttpQuery(url_child, params=None)
    html = query.get_page_html()
    elements = ElementPageChild(html)
    count_page = int(elements.count_page())  # количество динамически подгружаемых страниц
    print('Received all dynamically loaded pages:', count_page)
    #print(type(count_page))
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
    data_child = elements.get_child_element() # [(title, url)]
    print('Got elements child page: [(title, url)]')
    return data_child

#!
def get_id_troops(url_child, BASE_URL):
    """ select id from troops where url_child = ...; """
    
    child_url = url_child.replace(BASE_URL, '')
    conn = DbParser()
    id_troops = conn.select_id_troops(child_url)
    print('Got id referencing key table(troops):', id_troops)
    return id_troops

def mod_data_child(data_child, id_troops):
    """  """
    
    db_data_child = []
    for row in data_child:
        new_row = (id_troops, row[0], row[1])
        db_data_child.append(new_row)
    print('Generated data to be entered into the table(veterans): [(id_troops, title, url)]')
    return db_data_child

def save_data_child(db_data_child):
    """   """
    
    conn = DbParser()
    conn.insert_table_veterans(db_data_child)
    print('Saved data child page in database table: veterans')


def query_grandchild_page(BASE_URL, data_child):
    """ Get grandchild html page and elements """

    data_grandchild = []
    for row in data_child:
        # print(BASE_URL+row[1]) 
        url_grandchild = BASE_URL + row[1]
        query = HttpQuery(url_grandchild, params=None)
        html = query.get_page_html()
        elements = ElementPageGrandchildren(html)
        text = elements.get_grandchildren_element()
        data_grandchild.append((text, row[1]))
    print('Got data from grandchildren page')    
    return data_grandchild
 
def save_data_grandchild(data_grandchild):
    """  """

    conn = DbParser()
    conn.update_table_veterans(data_grandchild)
    print('Grandson page data saved in the database, table: veterans', '\n') 

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
    save_data_parent(data_parent)
    #url_child_one = get_url_child(BASE_URL, data_parent)

    for url_child in get_url_child(BASE_URL, data_parent):
            
        count_page = count_child(url_child)
        html_child = query_child_page(url_child, count_page)
        save_html_child(html_child, url_child)
        data_child = element_child_page(html_child) 
    
        id_troops = get_id_troops(url_child, BASE_URL) 
        db_data_child = mod_data_child(data_child, id_troops)
        save_data_child(db_data_child) 
    
        data_grandchild = query_grandchild_page(BASE_URL, data_child)
        save_data_grandchild(data_grandchild)
