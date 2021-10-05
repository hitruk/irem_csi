

import requests
from bs4 import BeautifulSoup
import re


class HttpQuery:

    def __init__(self, url, params):
        self.url = url
        self.params = params
        self.req = requests.get(url=self.url, params=self.params)

    def get_page_html(self):

        if self.req.status_code == 200:
            return self.req.text
        else:
            print('Server status code :',
                  self.req.status_code)
            return

class ElementPage:

    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(self.html, 'lxml')


class ElementPageParent(ElementPage):

    def get_parent_element(self):

        abc = self.soup.find('div', class_='sidebar-group__body').find('ul', class_='sidebar-nav').find_all('li')

        data = []  # список пункта меню: род войск

        for row in abc:
            try:
                title_one = row.find('a').text.strip()
                title = re.sub(r"( {1,})*([0-9])", "", title_one)
            except:
                title = ''
            try:
                url = row.find('a').get('href').strip()
            except:
                url = ''

            if url != '' and title != '':
                data.append((title, url))
        print(data)
        return data

class ElementPageChild(ElementPage):


    def get_child_element(self, id_troops):

        abc = self.soup.find('div', class_='content-blocks js-memoirs-items').find_all('div', class_='person person--light')
        data = []
        for row in abc:
            try:
                title = row.find('h4', class_='person__name').text  # имя_ветерана
            except:
                title = ''  # имя_ветерана
            try:
                url = row.find('div', class_='person__body').find('a').get('href')
            except:
                url = ''
            if title != '' and url != '':
                data.append((id_troops, title, url))
        return data


class ElementPageGrandchildren(ElementPage):


    def get_grandchildren_element(self):

        """Get text page and Search PHRASE"""

        abc = self.soup.find('div', class_='article__body').find_all('p')
        # на странице  отсутствует
        if abc == []:
            abc = self.soup.find('div', class_='article__body')
        text_one = []
        for row in abc:
            try:
                text = row.text.strip()
            except:
                text = ''
            text_one.append(text)
        text_fin = '\n'.join(text_one)
        # print(text_fin)
        return text_fin
