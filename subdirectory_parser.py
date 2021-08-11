"""
Module for parsing links to directories
prn=15000 -- Бытовая техника в Беларуси
https://www.kufar.by//listings?prn=16000 -- Компьютерная техника в Беларуси
"""


from bs4 import BeautifulSoup
import requests
import json
import re
import os.path
import hashlib


DEFAULT_URL = r'https://www.kufar.by/listings?rgn=all'
DEFAULT_PATH_DB = r"D:\Development\Coding\parser-kufar\DATA"
DEFAULT_NAME_DIRECTORY_DB = r"directory_link.json"
DEFAULT_NAME_SUBDIRECTORY_DB = r"directory_link.json"


def verification_link():
    pass


def creation_base():
    pass

def beautifulSoup_object_creation(url: str):
    """
    description:
        "Make a request from the link and collect subdirectory data from this page"
    args:
        url: str: "link"
    return:
        dict: "dictionary with links"
    """
    r = requests.get(url=url)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup


def subdirectory_parser(soup:BeautifulSoup):
    """
    description:
        ""
    args:
       
       
    yield:
        
        
    """
    sub = dict()
    for element in soup.findAll('li'):
        link = element.find('a').get('href')
        if re.search(pattern=r'cat', string=link):
            name = element.find('span').text
            id_hash = hashlib.sha224('{link}{name}'.format(link=link, name=name).encode('utf-8')).hexdigest()
            sub['{id_hash}'.format(id_hash=id_hash)] = dict(name=name, link=link)
    return sub


def link_extraction(path: str, name: str):
    """
    description:
        "function to retrieve links to directories from the database"
    args:
        path: str: "path to database"
        name: str: "database name"
    yield:
        "directory link"
    """
    with open(file='{a}/{b}'.format(a=path, b=name), mode='r', encoding='utf-8') as file:
        json_link = json.load(file)
    for name_link in json_link.items():
        yield name_link


def parser():
    subdirectory_dict = dict()
    for i in link_extraction(path=DEFAULT_PATH_DB, name=DEFAULT_NAME_DIRECTORY_DB):
        soup = beautifulSoup_object_creation(url=i[1]['link'])
        subdirectory_dict[i[0]] = subdirectory_parser(soup=soup)

    flag = os.path.isfile('{a}\{b}'.format(a=DEFAULT_PATH_DB, b=DEFAULT_NAME_SUBDIRECTORY_DB))
    if flag:
        verification_link()
    else:
        creation_base()


def main():
    parser()

if __name__ == '__main__':
    main()