import json
import time
from pathlib import Path

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from tqdm import tqdm

URL_BASE = 'https://openi.nlm.nih.gov/'
URL_SEARCH = 'https://openi.nlm.nih.gov/gridquery?it=xg&m={}&n={}'
URL_IMAGE = 'https://openi.nlm.nih.gov/detailedresult?img={}'

ROOT_DIR = Path(__file__).parent
IMAGES_FOLDER = ROOT_DIR / 'data' / 'images'
FILES_FOLDER = ROOT_DIR / 'data' / 'files'

START_NUMBER = 2601
END_NUMBER = 3000

DELAY_GRID = 10
DELAY_IMAGE = 1.5

driver = webdriver.Chrome(
    ROOT_DIR / 'driver' / 'chromedriver',
)

def get_soup(html_source: str) -> BeautifulSoup:
    """Returns the soup version of an html code"""
    return BeautifulSoup(html_source, "html.parser")

def get_source(driver) -> str:
    """Returns the source code of the webpage"""
    return driver.page_source

def get_image_urls(soup: BeautifulSoup) -> list:
    urls = []
    for item in soup.find_all('a'):
        if item.get('ng-href') is not None:
            if 'detailedresult' in item.get('ng-href'):
                urls.append(item.get('ng-href').split('&')[0].split('=')[-1])
    return urls

def reload_page(url: str) -> None:
    driver.get(url)

def get_image_url(soup_image):
    for item in soup_image.find_all(class_ = 'image ng-scope'):
        return item.find('img').get('src')
    return 

def download_image(url: str, images_folder, filename: str):
    file = images_folder / str(filename + '.png')
    with open(file, 'wb') as f:
        response = requests.get(url, stream=True)
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            f.write(block)

def get_grid_urls(url_search, start_number, end_number):
    url_grids = []
    for i in range(start_number, end_number, 100):
        url_grids.append(url_search.format(i, i+99))
    return url_grids

def get_title(soup):
    title = """"""
    for item in soup.find_all(class_ = 'title'):
        title += item.get_text() + '\n'
    return title

def get_abstract(soup):
    text = """"""
    for item in soup.find_all(class_ = 'col-sm-12 col-md-6 col-lg-6 right-side'):
        for line in item. get_text().split('\n'):
            if len(line) > 0:
                text += line + '\n'
    return text

def save_json(soup_image, files_folder, url):
    data = {
        "title": """{}""".format(get_title(soup_image)),
        "abstract": get_abstract(soup_image),
    }
    filename = files_folder / '{}.json'.format(url)
    with open(filename, "w+") as f:
        json.dump(data, f)


IMAGES_FOLDER.mkdir(parents=True, exist_ok=True)
FILES_FOLDER.mkdir(parents=True, exist_ok=True)

url_grids = get_grid_urls(URL_SEARCH, START_NUMBER, END_NUMBER)

for url_grid in tqdm(url_grids):
    driver.get(url_grid)
    time.sleep(DELAY_GRID)

    html_code = driver.page_source
    soup = get_soup(html_code)

    image_names = get_image_urls(soup)

    for image_name in tqdm(image_names, leave = False):
        reload_page(URL_IMAGE.format(image_name))
        time.sleep(DELAY_IMAGE)
        soup_image = get_soup(driver.page_source)
        url_ = URL_BASE + get_image_url(soup_image)
        download_image(url_, IMAGES_FOLDER, image_name)
        save_json(soup_image, FILES_FOLDER, image_name)

driver.close()
