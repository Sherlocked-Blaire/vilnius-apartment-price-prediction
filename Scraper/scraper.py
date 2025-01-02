from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

import pandas as pd

# Set up Chrome options (optional)
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--headless")

# Path to the ChromeDriver
chrome_driver_path = "/Users/blessing/Desktop/THESIS DUMP/chromedriver"

# Create the WebDriver instance
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

url_list = []
for page_number in range (0,128):
    default_url = "https://en.aruodas.lt/butai/vilniuje/puslapis/" +f"{page_number}/"
    driver.get(default_url)
    try:
        driver.find_element(By.XPATH,"/html/body/div[11]/div[2]/div/div[1]/div/div[2]/div/button[1]").click()
    except:
        pass 
    time.sleep(3)
    

    elements = driver.find_elements(By.CLASS_NAME, 'list-photo-v2')
    a_tags = []
    for element in elements:
        a_tags_in_element = element.find_elements(By.TAG_NAME, 'a')
        a_tags.extend(a_tags_in_element)

    for a_tag in a_tags:
        url_list.append(a_tag.get_attribute('href'))
    # print(url_list)
full_data = [] 

i=1

for url in url_list:
    driver.get(url)
    time.sleep(2)
    address = driver.find_element(By.CLASS_NAME, "obj-header-text")
    address = address.text.strip().split(', ')
    address_dict = {}        
    address_dict['city'] = address[0] or ""
    address_dict['neighbourhood'] = address[1] or ""
    address_dict['street'] = address[2]or ""
    price = driver.find_element(By.CLASS_NAME, "price-left")
    address_dict['price']=price.text

    desc = driver.find_element(By.CLASS_NAME, "obj-details")

    lines = desc.text.strip().splitlines()

    # Initialize an empty dictionary
    organized_data = {}

    # Initialize a variable to keep track of the key
    key = None

    # Iterate over the lines to build the dictionary
    for line in lines:
        if ":" in line:
            # If the line contains ":", it's a key
            key = line.strip(" :")  # Remove spaces and colons from key
        else:
            # If the line does not contain ":", it's a value for the previous key
            value = line.strip()
            if key:  # Check if we have a valid key
                address_dict[key] = value
                key = None  # Reset the key for the next item

    #

    proxy = driver.find_elements(By.CLASS_NAME, 'statistic-info-cell-main')

    for div in proxy:
        feature = div.text
        attr = feature.split("\n~ ")
        address_dict[attr[0]] = attr[1] or ""
    try:
        address_dict['crime'] = driver.find_element(By.CLASS_NAME,'arrow_line_left') .text or ""  
    except:
        address_dict['crime'] = ""

    full_data.append(address_dict)  
    print(f"Scraping page {i}"
          )
    i+=1

data= pd.DataFrame.from_dict(full_data, orient='columns')
data.to_csv("data_final9.csv", index =False, sep=';')   
    
    