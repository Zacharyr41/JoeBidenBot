from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

import constants as cts
import time

def get_driver() -> webdriver.Chrome:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver

def get_url_soup(driver : webdriver.Chrome, page_url : str) -> BeautifulSoup:
    driver.get(page_url)
    time.sleep(1)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    
    return soup

def get_links_from_page(driver: webdriver.Chrome, page_url: str) -> list[str]:
    result = []

    soup = get_url_soup(driver=driver, page_url=page_url)

    view_content_div = soup.find('div', class_='view-content')
    if view_content_div:
        views_row_divs = view_content_div.find_all(
            'div', class_=lambda value: value and value.startswith('views-row'))
        for div in views_row_divs:
            a_tags = div.find_all('a')
            for a in a_tags:
                href = a.get('href')
                if href:
                    result.append(href)
                    
    # Remove the Joe Biden People Page
    result = [x for x in result if x != cts.JOE_BIDEN_PAGE]
    return result

def get_speech_content(driver : webdriver.Chrome, page_url : str) -> tuple[str, str]:
    soup = get_url_soup(driver=driver, page_url=page_url)
    
    # Extract the date
    date_div = soup.find('div', class_='field-docs-start-date-time')
    date = date_div.find('span').text.strip() if date_div else None
    
    # Extract and concatenate paragraph texts
    content_div = soup.find('div', class_='field-docs-content')
    paragraphs = [p.text.strip() for p in content_div.find_all('p')] if content_div else []
    concatenated_paragraphs = '\n'.join(paragraphs)

    return (date, concatenated_paragraphs)
