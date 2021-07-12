"""
Module for parsing links to directories
"""

from bs4 import BeautifulSoup
import requests
import json
import re


DEFAULT_URL = r'https://www.kufar.by/listings'
DEFAULT_PATH_CATALOGS_DB = r'D:\Development\Coding\PAGE-KUFAR\DB'
DEFAULT_NAME_DB = r'directory-database'


def getWebsite(url: str):
    """
    description: 
            Makes a request to the web page.
    args:   url : url : "url address to page";
    return: "requests object"
    """   
    return requests.get(url)


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


def save_catalogs_in_db(catalogs: dict, path: str, directory_name: str):
    """
    description: 
            Creating a JSON object and saving it.
    args:   catalogs : dict : "Dictionary of directory names and links to them";
            path: str : Directory database storage path
    return: "JSON object of directories" 
    """
    path_db = r'{path}\{directory_name}.json'.format(path=path, directory_name=directory_name)
    with open(file=path_db, mode='w', encoding='utf-8') as file:
        json.dump(catalogs, file)

def parser():
    """
    the body of the module. basic function. (for import)
    """
    r = getWebsite(DEFAULT_URL)
    soup = BeautifulSoup(r.text, 'lxml')
    catalogs = search_links_directories(soup)
    # return  save_catalogs_in_db(catalogs=catalogs, path=DEFAULT_PATH_CATALOGS_DB)
    return catalogs

def main():
    """
    This is for an offline module call
    """
    catalogs = parser()
    print(r'save catlog in path: {path}\{name}'.format(path=DEFAULT_PATH_CATALOGS_DB, name=DEFAULT_NAME_DB))
    save_catalogs_in_db(catalogs=catalogs, path=DEFAULT_PATH_CATALOGS_DB, directory_name=DEFAULT_NAME_DB)
    print('end work!')


if __name__ == '__main__':
    main()
