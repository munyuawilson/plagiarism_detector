from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
from difflib import SequenceMatcher

import requests
import re


chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)

url="https://google.com"
text="Community & Support.Learn about our programs and get support.dsgsg sdfbjfj sdbjfbasj.ajf."
LINKS=[]

#get first two sentences to know the topic


#get links from google about the topic
def get_links(url,text):
        driver.get(url)
        driver.implicitly_wait(20)
        search=driver.find_element(By.CLASS_NAME,"gLFyf")
        search.send_keys(text)
        search.send_keys(Keys.RETURN)
        driver.implicitly_wait(20)
        #div with the <a> tags
        


        div_a=WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//*[@class='yuRUbf']" )))
        for div in div_a:

                tag=div.find_element(By.TAG_NAME,"a")
                link = tag.get_attribute("href")
                LINKS.append(link)

        print("Quiting Selenium ....")
        


        
        driver.quit()

def get_data():
        for l in LINKS:
                get=requests.get(l).text
                content=bs(get,'html.parser')
                content=content.body
                with open('data.txt','a', encoding='utf-8') as file:
                        file.write(content.text)

                
        print("Finished...")

def plag_detector():
        with open('data.txt','r',encoding='utf-8') as F:
                f=F.read()
                compare=SequenceMatcher(text,f)
                print(compare.ratio()*100)
                print("done")



