import time, os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def make_browser(headless=True):
    prefs = {'download.default_directory' : os.path.join(os.getcwd(), 'data', 'pdfs')}
    options = webdriver.chrome.options.Options()
    if headless: options.add_argument('--headless')
    options.add_argument('--disable-notifications')
    options.add_argument("--window-size=1920x1080")
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def download(links):
    driver = make_browser(True)
    for link in links:
        driver.get(link)
        time.sleep(5)
        driver.find_element(By.CSS_SELECTOR, '.SharedFileHeaderContentActions-download').click()
        time.sleep(10)
    driver.quit()
    
if __name__ == '__main__':
    pass