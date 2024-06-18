from fake_useragent import UserAgent
from stem.control import Controller
from stem import Signal
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


nbr_pages = 0
format_file =''
editor =''
lang = ''
autor = ''

proxy= {
    'http':'socks5h://127.0.0.1:9050',
    'https':'socks5h://127.0.0.1:9050',
}

tor_options  = {
    'proxy': {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050',
    }
}

global header 


def randomiseUserAgent():
    global header
    print('Changing the UserAgent now ! Getting new Values !')
    header =  UserAgent().random

def rotateIp():
    randomiseUserAgent()
    print('Changing the Ip now ! Getting new Values !')
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

    

def initBrowserDriver():
    rotateIp()
    options = webdriver.EdgeOptions()
    # options.add_argument("--headless=new")
    return webdriver.Edge(
        options=options,
        # header={'User-Agent': header},
        seleniumwire_options=tor_options,
    )

def getMetaData(webdriver):
    listElem =  webdriver.find_elements(by=By.CLASS_NAME,value="LrzXr kno-fv wHYlTd z8gr9e")
    print(listElem)
    global nbr_pages , format_file , editor , lang , autor
    nbr_pages = listElem[0].text
    format_file = listElem[1].text
    editor = listElem[2].text
    lang = listElem[3].text
    autor = listElem[4].text


driver = initBrowserDriver()

# Start
def start(link):
    global driver
    driver.get(link)
    print("Searching For The Book - "+driver.title )
    WebDriverWait(driver,10).until(lambda d: d.execute_script('return document.readyState') == 'complete')
    if(driver.current_url != link):
        return
    xpath_but = '//*[@id="main"]/div[1]/div[2]/div[1]/div/entity-page-viewport-entry/div'
    condition = EC.element_to_be_clickable((By.XPATH,xpath_but))
    WebDriverWait(driver, 30).until(condition)
    button = driver.find_element(by=By.XPATH,value=xpath_but)
    # getMetaData(driver)
    button.click()
    frame_loc = "iframe[class='fuHCCc']))"
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(By.CSS_SELECTOR, value=frame_loc))
    driver.switch_to.frame(driver.find_element(by=By.CSS_SELECTOR,value=frame_loc))
    time.sleep(5)
    



def main():
    link = input('Provide the Link for Google Books Book to Scrape: ')
    link = 'https://www.google.fr/books/edition/Ace_AWS_Certified_Solutions_Architect_As/2GPiEAAAQBAJ?hl=fr&gbpv=0'
    while(True):
        start(link)
        # downloadResources(extractedLinks)
        # updateLevel()
        rotateIp()



if(__name__=='__main__'):
    main()
