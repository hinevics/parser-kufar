from bs4 import BeautifulSoup
import requests
import json
import re
import os.path
import hashlib


DEFAULT_PATH_DB = r"D:\Development\Coding\parser-kufar\DATA"
DEFAULT_NAME_DIRECTORY_DB = r"directory_link.json"
DEFAULT_NAME_SUBDIRECTORY_DB = r"subdirectory_link.json"


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


def reading_links_subdirectories(path:str, name: str):
    with open(file='{path}/{name}'.format(path=path, name=name), mode='r', encoding='utf-8') as file:
        subdirlinks = json.load(fp=file)
    for directory_hash in subdirlinks.keys():
        for subdir in subdirlinks[directory_hash].values():
            yield subdir['name'], subdir['link']

def parser(path:str=DEFAULT_PATH_DB, name:str=DEFAULT_NAME_SUBDIRECTORY_DB):
    # for link in reading_links_subdirectories(path=DEFAULT_NAME_DIRECTORY_DB, name=DEFAULT_NAME_SUBDIRECTORY_DB)
    for i in reading_links_subdirectories(path=path, name=name):
        beautifulSoup_object_creation(url='{}/{}')

def main():
    parser()


if __name__ == '__main__':
    main()