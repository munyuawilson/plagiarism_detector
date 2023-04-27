from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import requests
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
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





#get first two sentences to know the topic

def get_text(user_input):
    token = nltk.sent_tokenize(user_input)
    if len(token) < 2:
        return False,"Error: Input must contain at least two sentences."
    else:
        return True,' '.join(token[:2])
#get links from google about the topic
def get_links(url,text,driver):
    LINKS=[]
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
    return LINKS

def get_data(LINKS):
    DATA_LIST=[]
    links_scrapped=[]
    for l in LINKS:
        
        try:
            if "youtube" in l:
                continue
            
            get=requests.get(l).text
            content=bs(get,'html.parser')
            content=content.body
            if content is not None:
                DATA_LIST.append(content.text)
                links_scrapped.append(l)
                print("great")
            else:
                print(f"Skipping {l} as content is None")
        except requests.exceptions.RequestException:
            print('error')

    print("Finished")
    return DATA_LIST,links_scrapped


def plag_detector(Userinput,DATA_LIST,links_scrapped):

    vectorizer = TfidfVectorizer()
    similarity_scores=[]
    tfidf = vectorizer.fit_transform(DATA_LIST + [Userinput])
    cosine_similarities = cosine_similarity(tfidf[:-1], tfidf[-1])
    max_similarity = cosine_similarities.max()
    similarity_scores.append(cosine_similarities.flatten())
    similarity_score=[]
    
    
    
    
    for i  in similarity_scores:
        i=i*100
        i=np.round(i,decimals=0)
        similarity_score.append(i)
    print(similarity_score)
         
    
        
    
    print('done!')
    print("Max Similarity Score:", round(max_similarity*100, 0))
    print("Similarity Scores List:", list(similarity_score))
    
    return round(max_similarity*100, 0), list(similarity_score),links_scrapped







                
       


