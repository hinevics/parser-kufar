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
        print(soup)


def main():
    parser()


if __name__ == '__main__':
    main()