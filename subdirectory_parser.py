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
DEFAULT_NAME_SUBDIRECTORY_DB = r"subdirectory_link.json"


def verification_link(sub_directory: dict, path: str, name: str):
    # Протестировать!!!
    with open('{path}/{name}'.format(path=path, name=name), mode='r', encoding='utf-8') as file:
        old_sub_directory = json.load(fp=file)
    for new_hash_id_directory in sub_directory.keys():
        if not(new_hash_id_directory in old_sub_directory.keys()):
            old_sub_directory[new_hash_id_directory] = sub_directory[new_hash_id_directory]
        else:
            for i in set(sub_directory[new_hash_id_directory].keys()).difference(set(old_sub_directory[new_hash_id_directory].keys())):
                old_sub_directory[new_hash_id_directory][i] = sub_directory[new_hash_id_directory][i]
    with open('{path}/{name}'.format(path=path, name=name), mode='r', encoding='utf-8') as file:
        json.dump(obj=old_sub_directory, fp=file)
    return old_sub_directory


def creation_base(subdirectory_dict : dict, path : str, name : str):
    """
    description:
        "create and write to file"
    args:
        subdirectory_dict: dict: "dictionary with links to subcategories";
        path: str: "path to db";
        name: str: "db name"
    """
    with open(file='{path}/{name}'.format(name=name, path=path), mode='w', encoding='utf-8') as file:
        json.dump(obj=subdirectory_dict, fp=file)


def beautifulSoup_object_creation(url: str):
    """
    description:
        "Make a request from the link and collect subdirectory data from this page"
    args:
        url: str: "link"
    return:
        dict: "soup object"
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
    # if flag:
    #     verification_link(sub_directory=subdirectory_dict, path=DEFAULT_PATH_DB, name=DEFAULT_NAME_SUBDIRECTORY_DB)
    # else:
    #     creation_base(subdirectory_dict=subdirectory_dict, name=DEFAULT_NAME_SUBDIRECTORY_DB, path=DEFAULT_PATH_DB)
    verification_link(sub_directory=subdirectory_dict, path=DEFAULT_PATH_DB, name=DEFAULT_NAME_SUBDIRECTORY_DB)
    return subdirectory_dict

def main():
    """
    This is to run the module separately
    """
    print('START PARSING ...')
    subdirectory_dict = parser()
    print('RESULT')
    # for i in subdirectory_dict.keys():
    #     print(subdirectory_dict[i])
    print(r'save catlog in path: {path}\{name}'.format(path=DEFAULT_PATH_DB, name=DEFAULT_NAME_SUBDIRECTORY_DB))
    print('PARSING COMPLETED')


if __name__ == '__main__':
    main()