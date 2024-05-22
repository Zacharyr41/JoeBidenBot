from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

def get_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    