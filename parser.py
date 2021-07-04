"""
1. Попробовать сделать CLI из этого чтоб раздеить процесс выгрузки страниц и парсинг!
"""
from bs4 import BeautifulSoup
import requests

# default variables 
DEFAULT_HEADER = {'user-agent': r'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
DEFAULT_URL_CATALOG = r'https://www.kufar.by/listings?cat=17010&ot=1&query=%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9&rgn=all'
DEFAULT_PATH_FILE_WEB_PAGE = r'D:\Development\Coding\PAGE-KUFAR'
DEFAULT_NAME = r'page'
DEFAULT_CLASS_ = r'kf-FXM-0a457'

# global variables
NUMBER_LINKS_PAGES_CATALOG = {
    '1': r'https://www.kufar.by/listings?cat=17010&ot=1&query=%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9&rgn=all&cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6MX0%3D'
}


def getWebsite(url:str):
    r = requests.get(url=url, headers=DEFAULT_HEADER)
    return r


def saveHTML(html:str, name:str, path: str):
    with open(file=r'{path}\{name}'.format(path=path, name=name), encoding='utf-8', mode='w') as file:
        file.write(html)


def openFileHTML(path:str, name:str):
    with open(file=r'{path}\{name}'.format(path=path, name=name), mode='r', encoding='utf-8') as file:
        return file.read()

def search_link_page(soup_obj: BeautifulSoup):
    numbers_webpages = soup_obj.find_all('a', class_=DEFAULT_CLASS_)
    # Get page numbers and links
    for i in numbers_webpages:
        if not (i.text in NUMBER_LINKS_PAGES_CATALOG.keys()):
            NUMBER_LINKS_PAGES_CATALOG[i.text] = 'https://www.kufar.by/' + i.get('href')
        

def main():
    # r = getWebsite(url=DEFAULT_URL_CATALOG)
    # saveHTML(html=r.text, path=DEFAULT_PATH_FILE_WEB_PAGE, name=DEFAULT_NAME)
    print('start bield page 1')
    page = openFileHTML(path=DEFAULT_PATH_FILE_WEB_PAGE, name=DEFAULT_NAME)
    soup = BeautifulSoup(markup=page, features='lxml')
    search_link_page(soup_obj=soup) # search for links on a page
    
    
    
if __name__ == '__main__':
    main()