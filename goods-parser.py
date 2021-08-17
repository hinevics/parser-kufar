from bs4 import BeautifulSoup
import requests
import json
import re
import os.path
import hashlib

DEFAULT_HEADER = {'user-agent': r'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
DEFAULT_URL = r'https://www.kufar.by'
DEFAULT_PATH_DB = r"D:\Development\Coding\parser-kufar\DATA"
DEFAULT_NAME_DIRECTORY_DB = r"directory_link.json"
DEFAULT_NAME_SUBDIRECTORY_DB = r"subdirectory_link.json"


# links to pages in this category
NUMBER_LINKS_PAGES_CATALOG = {}
# products from pages
GOODS = []

# It's in development. 
def parser_location(location: str):
    """
    Highlights location and coordinates
    """
    pass

# It's in development. 
def parser_data_and_time(data_time: str):
    """
    Highlights time and date. Converts to UTC
    """
    return data_time


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


def search_link_page(soup_obj: BeautifulSoup):
    """
    Search for links to other catalog pages
    """
    numbers_webpages = soup_obj.find('div', {'data-name':'listings-pagination'}).find_all('a')
    # Get page numbers and links
    for i in numbers_webpages:
        NUMBER_LINKS_PAGES_CATALOG[i.text] = 'https://www.kufar.by/' + i.get('href')


def beautifulSoup_object_creation(url: str, header:dict):
    """
    description:
        "Make a request from the link and collect subdirectory data from this page"
    args:
        url: str: "link"
        header: dict: "it is user-agent"
    return:
        dict: "soup object"
    """
    r = requests.get(url=url, headers=header)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup


def reading_links_subdirectories(path:str, name: str):
    with open(file='{path}/{name}'.format(path=path, name=name), mode='r', encoding='utf-8') as file:
        subdirlinks = json.load(fp=file)
    for directory_hash in subdirlinks.keys():
        for subdir in subdirlinks[directory_hash].values():
            yield subdir['link']

def parser(path:str=DEFAULT_PATH_DB, name:str=DEFAULT_NAME_SUBDIRECTORY_DB, d_url:str=DEFAULT_URL, header:dict=DEFAULT_HEADER):
    # for link in reading_links_subdirectories(path=DEFAULT_NAME_DIRECTORY_DB, name=DEFAULT_NAME_SUBDIRECTORY_DB)
    for link in reading_links_subdirectories(path=path, name=name):
        soup = beautifulSoup_object_creation(url='{d_url}/{link}'.format(d_url=d_url, link=link), header=header)
        search_link_page(soup_obj=soup)
        max_page = int(max(NUMBER_LINKS_PAGES_CATALOG.keys()))
        collection_ads(soup_obj=soup)
        print(len(GOODS))
        break

def main():
    parser()


if __name__ == '__main__':
    main()