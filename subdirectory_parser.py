"""
Module for parsing links to directories
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


def parser():
    # page_parser(url=)
    pass


def main():
    parser()

if __name__ == '__main__':
    main()