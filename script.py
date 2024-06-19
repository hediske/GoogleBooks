from fake_useragent import UserAgent
from stem.control import Controller
from stem import Signal
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from urllib.parse import urlparse, parse_qs

import requests


extracted_links = []
pages = []
header = None

proxy= {
    'http':'socks5h://127.0.0.1:9050',
    'https':'socks5h://127.0.0.1:9050',
}

tor_options  = {
    'connection_timeout': None,
    'proxy': {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050',
        'no_proxy': 'localhost, 127.0.0.1'
    },
    'verify_ssl': False


}



def extract_pages(url_st):
    global header
    if(url_st):
        url = urlparse(url_st)
        query_params = parse_qs(url.query)
        header =  query_params.get("pg", [""])[0]


def randomiseUserAgent():
    print('Changing the UserAgent now ! Getting new Values !')
    return UserAgent().random

def rotateIp():
    header= randomiseUserAgent()
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
        seleniumwire_options=tor_options,
    )

def getMetaData(webdriver):
    listElem =  webdriver.find_elements(by=By.CLASS_NAME,value="LrzXr kno-fv wHYlTd z8gr9e")
    print(listElem)




driver = initBrowserDriver()

# Start
def start(link):
    driver.get(link)
    print("Searching For The Book - "+driver.title )

    #waiting for initial page loading
    # WebDriverWait(driver,10).until(lambda d: d.execute_script('return document.readyState') == 'complete')


    # for _ in range(3):
    #     if(driver.current_url != link and driver.title.find('www.google') == -1):
    #         print("Google Blocked Access to this ip , Retrying in 5 seconds")
    #         time.sleep(2.5)
    #         return
    #     time.sleep(2.5)


    
    try:
        xpath_but = '//*[@id="main"]/div[1]/div[2]/div[1]/div/entity-page-viewport-entry/div'
        WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,xpath_but))).click()
        print('Clicked on button to advance ! Generating Pages for This IP successfully')
    except Exception as e:
        print("Error in Clicking on button to advance : Retrying again")
        return
    try:

        print("Proceeding for File Downloading")
        for _ in range(10):
            try:
                frame = driver.find_element(by=By.CSS_SELECTOR,value="#s7Z8Jb")
                if(frame.get_attribute('src')):
                    break
                print("Lazy Loading issue ; Repeating waiting for another time ")
                time.sleep(5)
            except:
                time.sleep(5)
        # WebDriverWait(driver,25).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"#s7Z8Jb")))
        
        driver.switch_to.frame(frame)
        print("Switched to frame successfully")

        test_block = len(driver.find_elements(by=By.XPATH,value="/html/body/div[1]/table")) > 0 
        print("You are blocked by Google : ",test_block)
        if(test_block):
            print("Google recognized automatic access , Retrying in 5 seconds")
            return      
        for _ in range(5):
            try:     
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'overflow-scrolling')))
                break
            except(Exception):
                print(Exception)
                pass

        print("File finally Loaded successfully")

        result = driver.execute_async_script('''
            console.log("Scraping Started !");

            let book = document.getElementById("viewport");
            let observer = null;
            let targets = [];
            let links = [];
            let scroll = document.getElementsByClassName("overflow-scrolling");
            let scrollHeight = scroll[0].scrollHeight;
            let scrollCount = 0;
            let scrollAmount = 1400;
            let scrollInterval = "" ;
                              
            let callback = function (mutationsList, observer) {
                for (let mutation of mutationsList) {
                if (mutation.type == "childList") {
                    targets = mutation.target.getElementsByTagName("img");

                    if (targets) {
                    for (let target of targets) {
                        if(target.src!=="" && links.indexOf(target.src) == -1){
                            links.push(target.src);}
                    }
                    }
                }
                }
            };                  
                        

            let movePage = function (callback){
                setTimeout(function() {
                    scrollValue = Math.floor( ( scrollAmount - 50 + 1 ) * Math.random()  + 50);
                    scrollCount += scrollValue;
                    if(scrollCount < scrollHeight-500){
                        scroll[0].scrollBy(0,scrollValue);
                        movePage(callback);
                    }
                    else{
                        console.log("Scraping Completed !");
                        callback()
                    }
            }, Math.random()*200+400);
            }
                              
            observer = new MutationObserver(callback);
            observer.observe(book, {
                attributes: true,
                childList: true,
                subtree: true,
            });
        movePage(function() {
            console.log(links); 
            return links
        });
    
                                                  
        ''')
        for link in result:
            pg  = extract_pages(link)
            if(pg is not None and pg not in pages):
                pages.append(pg)    
                extracted_links.append(link)
                print(link)
            

    except(Exception) as e:
        print("Error happend when scraping using this ip , Retrying in seconds")
        print(e)
        return
    



def main():
    # link = input('Provide the Link for Google Books Book to Scrape: ')
    link = 'https://www.google.fr/books/edition/Ace_AWS_Certified_Solutions_Architect_As/2GPiEAAAQBAJ?hl=fr&gbpv=0'
    while True:
        start(link)
        # downloadResources(extractedLinks)
        # updateLevel()
        rotateIp()



if(__name__=='__main__'):
    main()
