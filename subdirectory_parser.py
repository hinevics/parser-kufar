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
    subdirectory = dict(header=soup.find('h1').text)
    for element in soup.findAll('li'):
        print(element.find('a').get('href'))
        print(element.find('span').text)
        break

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
    for i in link_extraction(path=DEFAULT_PATH_DB, name=DEFAULT_NAME_DIRECTORY_DB):
        # Тут добавить то как будут парситься все возможные подкаталоги
        key_hash = i[0]
        soup = beautifulSoup_object_creation(url=i[1]['link'])
        subdirectory_parser(soup=soup)
        print(i)
        break
    # soup = beautifulSoup_object_creation(url='https://www.kufar.by//listings?prn=15000')
    # # parser_headers(soup=soup)
    # subdirectory_parser(soup=soup)

def main():
    parser()

if __name__ == '__main__':
    main()