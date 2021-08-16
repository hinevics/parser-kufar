from bs4 import BeautifulSoup
import requests
import json
import re
import os.path
import hashlib


DEFAULT_PATH_DB = r"D:\Development\Coding\parser-kufar\DATA"
DEFAULT_NAME_DIRECTORY_DB = r"directory_link.json"
DEFAULT_NAME_SUBDIRECTORY_DB = r"subdirectory_link.json"


def reading_links_subdirectories(path:str, name: str):
    with open(file='{path}/{name}'.format(path=path, name=name), mode='r', encoding='utf-8') as file:
        subdirlinks = json.load(fp=file)
    print(subdirlinks)


def parser():
    # for link in reading_links_subdirectories(path=DEFAULT_NAME_DIRECTORY_DB, name=DEFAULT_NAME_SUBDIRECTORY_DB)
    reading_links_subdirectories(path=DEFAULT_NAME_DIRECTORY_DB, name=DEFAULT_NAME_SUBDIRECTORY_DB)

def main():
    parser()


if __name__ == '__main__':
    main()