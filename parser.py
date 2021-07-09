"""
1. Попробовать сделать CLI из этого чтоб раздеить процесс выгрузки страниц и парсинг!
"""
from bs4 import BeautifulSoup
import requests

# default variables 
DEFAULT_HEADER = {'user-agent': r'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
DEFAULT_URL_CATALOG = r'https://www.kufar.by/listings?cat=17010&rgn=all'
DEFAULT_PATH_FILE_WEB_PAGE = r'D:\Development\Coding\PAGE-KUFAR'
DEFAULT_NAME = r'page1'


# global variables
# links to pages in this category
NUMBER_LINKS_PAGES_CATALOG = {}
# products from pages
GOODS = []


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
    """
    Search for links to other catalog pages
    """
    numbers_webpages = soup_obj.find('div', {'data-name':'listings-pagination'}).find_all('a')
    # Get page numbers and links
    for i in numbers_webpages:
        NUMBER_LINKS_PAGES_CATALOG[i.text] = 'https://www.kufar.by/' + i.get('href')

def parser_data_and_time(data_time: str):
    """
    Highlights time and date. Converts to UTC
    """
    return data_time

def parser_location(location: str):
    """
    Highlights location and coordinates
    """
    pass


def collection_ads(soup_obj: BeautifulSoup):
    article = soup_obj.find('article')
    a = article.find_all('a', {'target': '_blank'})
    for i in range(len(a)):
        link_product = a[i].get('href')
        photo_link = a[i].find('img').get('data-src')  # link in the photo
        name_product = a[i].find('img').get('alt')
        data_time = parser_data_and_time(a[i].find('span').text)
        info1 = a[i].find('div').find_next_sibling()
        description = info1.find('h3').text
        info2 = info1.find('div').find_next_sibling()
        price = info2.find('div').find('span').text
        location = info2.find('div').find_next_sibling().find('span').text
        GOODS.append(dict(
            link_product=link_product,
            photo_link=photo_link,
            name_product=name_product,
            data_time=data_time,
            description=description,
            price=price,
            location=location))


def parser(url):
    r = getWebsite(url=url)
    soup = BeautifulSoup(markup=r.text, features='lxml')
    search_link_page(soup_obj=soup)
    max_page = int(max(NUMBER_LINKS_PAGES_CATALOG.keys()))
    list_not_keys = []
    i = 2
    while i < max_page:
        try:
            r = getWebsite(url=NUMBER_LINKS_PAGES_CATALOG[str(i)])
            soup = BeautifulSoup(markup=r.text, features='lxml')
            search_link_page(soup_obj=soup)
            collection_ads(soup_obj=soup)
            i += 1
        except KeyError:
            r = getWebsite(url=NUMBER_LINKS_PAGES_CATALOG[str(i-1)])
            soup = BeautifulSoup(markup=r.text, features='lxml')
            search_link_page(soup_obj=soup)
            
    print(GOODS)

def main():
    # parser(url='https://www.kufar.by/listings?rgn=all')
    r = getWebsite(url='https://www.kufar.by/listings?rgn=all')
    soup = BeautifulSoup(markup=r.text, features='lxml')
    search_link_page(soup_obj=soup)
    collection_ads()
    
if __name__ == '__main__':
    main()