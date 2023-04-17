from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import requests
import nltk
from nltk.tokenize import word_tokenize
from nltk.metrics import jaccard_distance
nltk.download('punkt')

chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)

url="https://google.com"
text="Community & Support.Learn about our programs and get support.dsgsg sdfbjfj sdbjfbasj.ajf."
LINKS=[]
DATA_LIST=[]

#get first two sentences to know the topic

def get_text(user_input):
            token=nltk.sent_tokenize(user_input)
            return token[0]
#get links from google about the topic
def get_links(url,text,driver):
    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        search = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "gLFyf")))
        search.send_keys(text)
        search.send_keys(Keys.RETURN)
        driver.implicitly_wait(5)

        div_a=WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//*[@class='yuRUbf']" )))
        for div in div_a:
            tag=div.find_element(By.TAG_NAME,"a")
            link = tag.get_attribute("href")
            LINKS.append(link)

        driver.quit()
    print("Quiting Selenium ....")

def get_data():
    for l in LINKS:
        try:
            if "youtube" in l:
                    continue
            get=requests.get(l).text
            content=bs(get,'html.parser')
            content=content.body
            DATA_LIST.append(content.text)
        except requests.exceptions.RequestException:
            print('error')

                
    print("Finished...")

def plag_detector(Userinput):
        '''with open('data.txt','r',encoding='utf-8') as file:
                f=file.read()'''
                
                
                
                
        def jaccard_similarity(text1, text2):
                words1 = set(word_tokenize(text1.lower()))
                words2 = set(word_tokenize(text2.lower()))
                return 1 - jaccard_distance(words1, words2)
        similarity_scores=[]
        for DATA in DATA_LIST:
                similarity_score = jaccard_similarity(Userinput, DATA)
                similarity_scores.append(similarity_score)
        print('done!')
        print(similarity_scores)
        print(round(max(similarity_scores)*100,0))
        return round(max(similarity_scores)*100,0)

                
       


