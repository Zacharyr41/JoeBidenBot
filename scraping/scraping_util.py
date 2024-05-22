from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

import constants as cts


def get_driver() -> webdriver.Chrome:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver


def get_links_from_page(driver: webdriver.Chrome, page_url: str) -> list[str]:
    result = []
    driver.get(page_url)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

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


if __name__ == "__main__":
    my_driver = get_driver()
    my_url = cts.SPEECHES_RESULT_PAGE + "0"
    res_links = get_links_from_page(driver=my_driver, page_url=my_url)
    print("Res Links Len: ", len(res_links))
    my_driver.quit()