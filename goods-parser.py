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
DEFAULT_NAME_GOODS_DB = r'goods.json'


# links to pages in this category
NUMBER_LINKS_PAGES_CATALOG = {}
# products from pages
GOODS = []
DB = dict()

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
   , Search for links to other catalog pages
    """
    if soup_obj.find('div', {'data-name':'listings-pagination'}) is None:
        print(soup_obj)
        input()
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
        for subdir in subdirlinks[directory_hash].items():
            yield (directory_hash, subdir[0], subdir[1]['link'])
        GOODS.clear()
        NUMBER_LINKS_PAGES_CATALOG.clear()


def create_goods_db(hash_dir:str, hash_subdir:str):
    if not (hash_dir in DB.keys()):
        DB[hash_dir] = {hash_subdir: GOODS}
    else:
        DB[hash_dir].update({hash_subdir:GOODS})


def save_db_goods(path:str, name:str):
    with open(file='{path}/{name}'.format(path=path, name=name), mode='w', encoding='uth=f-8') as file:
        json.dump(obj=DB, fp=file)


def parser(path:str=DEFAULT_PATH_DB,
           name_sub:str=DEFAULT_NAME_SUBDIRECTORY_DB,
           d_url:str=DEFAULT_URL,
           header:dict=DEFAULT_HEADER,
           name_goods:str=DEFAULT_NAME_GOODS_DB):
    for dir_subdir_link in reading_links_subdirectories(path=path, name=name_sub):
        dirhash = dir_subdir_link[0]
        subdirhash = dir_subdir_link[1]
        link = dir_subdir_link[2]
        soup = beautifulSoup_object_creation(url='{d_url}/{link}'.format(d_url=d_url, link=link), header=header)
        search_link_page(soup_obj=soup)
        max_page = int(max(NUMBER_LINKS_PAGES_CATALOG.keys(), key=lambda x: int(x) if x != '' else 0))
        i = 2
        while i < max_page:
            try:
                soup = beautifulSoup_object_creation(url=NUMBER_LINKS_PAGES_CATALOG[str(i)], header=header)
                search_link_page(soup_obj=soup)
                collection_ads(soup_obj=soup)
                i += 1
            except KeyError:
                soup = beautifulSoup_object_creation(url=NUMBER_LINKS_PAGES_CATALOG[str(i-1)], header=header)
                search_link_page(soup_obj=soup)
        create_goods_db(hash_dir=dirhash, hash_subdir=subdirhash)
        
        if i == 3:
            print('stop')
            break
    save_db_goods(path=path, name=name_goods)
    
    # for dir_subdir_link in reading_links_subdirectories(path=path, name=name):
    #     dirhash = dir_subdir_link[0]
    #     subdirhash = dir_subdir_link[1]
    #     link = dir_subdir_link[2]
    #     saver_goods(goods=[link], hash_dir=dirhash, hash_subdir=subdirhash)


def main():
    parser()


if __name__ == '__main__':
    main()