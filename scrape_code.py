
import json
import time

from selenium import webdriver
from time import sleep


from bs4 import BeautifulSoup
import requests
import pandas as pd

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from tqdm import tqdm_notebook

base_url = "https://ca.amazon.com"


def get_soup(url):
    return BeautifulSoup(requests.get(url).content, 'lxml')

data = {}

soup = get_soup(base_url + '/categories')

#This loop is for the name of the category and sub categories.
for category in soup.findAll('div', {'class': 'subCategory___BRUDy'}): #this returns a set of elements inside 
    name = category.find('span', {'class': 'topCategoryItemText___N3sdL'}).text #find() is same as find_all(n=1) -stopsa after first match.
    name = name.strip()
    data[name] = {}  
    sub_categories = category.find('div', {'class': 'subCategoryList___r67Qj'})
    
    for sub_category in sub_categories.findAll('div', {'class': 'subCategoryItem___3ksKz'}):
        sub_category_name = sub_category.find('span', {'class': 'subCategoryItemText___2nAeo'}).text 
        sub_category_uri = sub_category.find('a')['href']
        data[name][sub_category_name] = sub_category_uri

def extract_company_urls_form_page():
    a_list = driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div/div[2]/section/div[3]/a[2]/div/div[2]/div[1]/div[1]')
    urls = [a.get_attribute('href') for a in a_list]
    dedup_urls = list(set(urls))
    return dedup_urls

def go_next_page():
    try:
        button = driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div[2]/section/nav/a[4]')
        return True, button
    except NoSuchElementException:
        return False


#--------this part is undone yet-------------------------#

# options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('start-maximized')
# options.add_argument('disable-infobars')
# options.add_argument("--disable-extensions")

# prefs = {"profile.managed_default_content_settings.images": 2}
# options.add_experimental_option("prefs", prefs)
# driver = webdriver.Chrome()

# timeout = 3

# company_urls = {}
# for category in tqdm_notebook(data):
#     for sub_category in tqdm_notebook(data[category], leave=False):
#         company_urls[sub_category] = []

#         url = base_url + data[category][sub_category] + "?numberofreviews=0&timeperiod=0&status=all"
#         driver.get(url)
#         try: 
#             element_present = EC.presence_of_element_located(
#                 (By.CLASS_NAME, 'category-business-card card'))
            
#             WebDriverWait(driver, timeout).until(element_present)
#         except:
#             pass
    
#         next_page = True
#         c = 1
#         while next_page:
#             extracted_company_urls = extract_company_urls_form_page()
#             company_urls[sub_category] += extracted_company_urls
#             next_page, button = go_next_page()
            
#             if next_page:
#                 c += 1
#                 next_url = base_url + data[category][sub_category] + "?numberofreviews=0&timeperiod=0&status=all" + f'&page={c}'
#                 driver.get(next_url)
#                 try: 
#                     element_present = EC.presence_of_element_located(
#                         (By.CLASS_NAME, 'category-business-card card'))
                    
#                     WebDriverWait(driver, timeout).until(element_present)
#                 except:
#                     pass

#----------write a file below------------#

with open('scraped_categories.json', 'w') as outfile:
    json.dump(data, outfile)

#-----------make df of consolidatee data------------------#

# consolidated_data = []

# for category in data:
#     for sub_category in data[category]:
#         for url in company_urls[sub_category]:
#             consolidated_data.append((category, sub_category, url))

# df_consolidated_data = pd.DataFrame(consolidated_data, columns=['category', 'sub_category', 'company_url'])

# df_consolidated_data.to_csv('./exports/consolidate_company_urls.csv', index=False)