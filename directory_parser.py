"""
Module for parsing links to directories
"""

from bs4 import BeautifulSoup
import requests
import json
import re
import os.path
import hashlib


# DEFAULT_PATH_CATALOGS_DB = r'D:\Development\Coding\PAGE-KUFAR\DB'
# DEFAULT_NAME_DB = r'directory-database'
DEFAULT_URL = r'https://www.kufar.by/listings?rgn=all'
DEFAULT_PATH_DIRECTORY_DB = r"D:\Development\Coding\parser-kufar\DATA"
DEFAULT_NAME_DIRECTORY_DB = r"directory_link.json"


def search_links_directories(soup: BeautifulSoup): 
    """
    to-do:
            1. Сделать проверку на наличия прямой ссылки!
    description:
            search for catalogs on the galvanized page of the site
    args:   soup: BeautifulSoup object: "объект класс ... полученный с сайта"
    return: "a dictionary with the names of directories and links to these directories"
    """
    left_menu = soup.find('div', {'data-name': 'left_menu'})
    li = left_menu.find_all('li')
    catalogs = dict()
    for i_li in li:
        link = i_li.find('a').get('href')
        text = i_li.find('span').text
        if not re.match(pattern='http', string=link):
            catalogs[text] = r'https://www.kufar.by/' + link
    return catalogs


# def save_catalogs_in_db(catalogs: dict, path: str, directory_name: str):
#     """
#     description: 
#             Creating a JSON object and saving it.
#     args:   catalogs : dict : "Dictionary of directory names and links to them";
#             path: str : Directory database storage path
#     return: "JSON object of directories" 
#     """
#     path_db = r'{path}\{directory_name}.json'.format(path=path, directory_name=directory_name)
#     with open(file=path_db, mode='w', encoding='utf-8') as file:
#         json.dump(catalogs, file)

# def parser():
#     """
#     the body of the module. basic function. (for import)
#     """
#     r = getWebsite(DEFAULT_URL)
#     soup = BeautifulSoup(r.text, 'lxml')
#     catalogs = search_links_directories(soup)
#     # return  save_catalogs_in_db(catalogs=catalogs, path=DEFAULT_PATH_CATALOGS_DB)
#     return catalogs

def page_parser(url: str):
    """
    description:
        "Make a request from the link and collect catalog data from this page"
    args:
        url: str: "link"
    return:
        dict: "dictionary with links"
    """
    r = requests.get(url=url)
    soup = BeautifulSoup(r.text, 'lxml')
    catalogs = search_links_directories(soup)
    return catalogs


def verification_link(link_directory: dict, path: str, name: str):
    """
    description:
        "Checking links for repetition"
    args:
        link_directory: dict: "Directory link dictionary"
    """
    with open(file='{path}\{name}'.format(path=path, name=name), mode='r', encoding='utf-8') as file:
        links_directories_verification = json.load(file)
        for new_name_link in link_directory.items():
            new_hash_link = hashlib.sha224(new_name_link[1].encode('utf-8')).hexdigest()
            if  not(new_hash_link in links_directories_verification.keys()):
                links_directories_verification[new_hash_link] = dict(name=new_name_link[0], link=new_name_link[1])
                print('this link added: {a}'.format(a=new_name_link[1]))
            else:
                print('This link is in the database: {a}'.format(a=new_name_link[1]))


def creation_base(link_directory: dict, path: str, name: str):
    """
    description:
        "creating a database JSON object"
    args:
        link_directory: dict: "Directory link dictionary"
    return "JSON object"
    """
    with open(file='{path}\{name}'.format(path=path, name=name), mode='w', encoding='utf-8') as file:
        """
        {
            'hash': {
                'name': 'name',
                'link': 'link'
            }
        }
        """
        links_directories_writing_json = dict()
        for name_link in link_directory.items():
            hash_link = hashlib.sha224(name_link[1].encode('utf-8')).hexdigest()
            if not (hash_link in links_directories_writing_json.keys()):
                links_directories_writing_json[hash_link] = dict(name=name_link[0], link=name_link[1])
            else:
                print('this link has been created: {a}'.format(a=name_link[1]))
        print(links_directories_writing_json)
        json.dump(links_directories_writing_json, file)


def main():
    # """
    # This is for an offline module call
    # """
    # catalogs = parser()
    # print(r'save catlog in path: {path}\{name}'.format(path=DEFAULT_PATH_CATALOGS_DB, name=DEFAULT_NAME_DB))
    # save_catalogs_in_db(catalogs=catalogs, path=DEFAULT_PATH_CATALOGS_DB, directory_name=DEFAULT_NAME_DB)
    # print('end work!')
    
    # parsing
    link_directory = page_parser(url=DEFAULT_URL)
    flag = os.path.isfile('{a}\{b}'.format(a=DEFAULT_PATH_DIRECTORY_DB, b=DEFAULT_NAME_DIRECTORY_DB))
    if flag:
        # File find
        verification_link(link_directory=link_directory, name=DEFAULT_NAME_DIRECTORY_DB, path=DEFAULT_PATH_DIRECTORY_DB)
    else:
        # File not found 
        creation_base(link_directory=link_directory, name=DEFAULT_NAME_DIRECTORY_DB, path=DEFAULT_PATH_DIRECTORY_DB)

if __name__ == '__main__':
    main()