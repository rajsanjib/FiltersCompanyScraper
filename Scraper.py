from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, random, csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

CHROME_PATH = '/usr/bin/google-chrome-stable'
CHROMEDRIVER_PATH = './chromedriver'
WINDOW_SIZE = "1920,1080"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = CHROME_PATH

driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                          chrome_options=chrome_options
                         )

with open('data.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    for i in range(1,100):
        url = f'https://www.alibaba.com/catalog/air-filter_cid100006810?page={i}'
        driver.get(url)
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME,"ui2-pagination-pages"))
        )
        results = driver.find_elements_by_class_name('organic-gallery-offer-outter')
        for one in results:
            url = one.find_element_by_class_name('organic-gallery-offer__seller-company').get_attribute("href")
            company_name = one.find_element_by_class_name('organic-gallery-offer__seller-company').text
            writer.writerow([company_name, url])

data = pd.read_csv('data.csv')
urls = data['url']
site = []
for url in urls:
    driver.get(url)
    # WebDriverWait(driver,7).until(
    #     EC.presence_of_element_located((By.CLASS_NAME,"//*[contains(text(), 'Send')]"))
    # )
    try:
        site.append(driver.find_elements_by_xpath("//div[contains(text(), 'http://')]")[0].text)
    except:
        site.append('NA')

websites = data["website"]
email = []
for w in websites:
    print(w)
    if w is not 'NA':
        driver.get(w)
        doc = driver.page_source
        emails.append(re.findall(r'[\w\,-]+@[\w\.-]+', doc))
    else:
        email.append('NA')
