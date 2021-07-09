from bs4 import BeautifulSoup
import requests
import json


DEFAULT_URL = r'https://www.kufar.by/listings'
DEFAULT_PATH_CATALOGS_DB = r''


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
    description:
            search for catalogs on the galvanized page of the site
    args:   soup: BeautifulSoup object: "объект класс ... полученный с сайта"
    return: "a dictionary with the names of directories and links to these directories"
    """
    left_menu = soup.find('div', {'data-name': 'left_menu'})
    li = left_menu.find_all('li')
    catalogs = dict()
    for i_li in li:
        catalogs[i_li.find('span').text] = r'https://www.kufar.by/' + i_li.find('a').get('href')
    return catalogs


def save_catalogs_in_db(catalogs: dict, path: str):
    """
    description: 
            Creating a JSON object and saving it.
    to-do:
            1. make a check for the presence of the base
            2. make a reconciliation of keys
            3. make a verification of links 
    args:   catalogs : dict : "Dictionary of directory names and links to them";
            path: str : Directory database storage path
    return: "JSON object of directories" 
    """
    pass


def parser():
    """
    the body of the module. basic function. (for import)
    """
    r = getWebsite(DEFAULT_URL)
    soup = BeautifulSoup(markup=requests.text)
    catalogs = search_links_directories(soup)
    save_catalogs_in_db = 
    

def main():
    """
    This is for an offline module call
    """
    parser()

    
if __name__ == '__main__':
    main()
