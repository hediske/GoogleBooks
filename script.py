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


extracted_links = set()
new_links = set()
pages = []
header = None
link =""
name =""

def interceptor(request):
    del request.headers['User-Agent']
    request.headers['User-Agent'] = header


proxy= {
    'http':'socks5h://tor-privoxy:9050',
    'https':'socks5h://tor-privoxy:9050',
}

tor_options  = {
    'connection_timeout': None,
    'proxy': {
        'http': 'socks5h://tor-privoxy:9050',
        'https': 'socks5h://tor-privoxy:9050',
        'no_proxy': 'localhost, tor-privoxy'
    },
    'verify_ssl': False

}


def updateImages():
    global new_links
    for image in new_links:
        r = requests.get(image)
        with open(f'{name}/{extract_pages(image)}', 'wb') as f:
            f.write(r.content)
    new_links.clear()




def extract_pages(url_st):
    global header
    if(url_st):
        url = urlparse(url_st)
        query_params = parse_qs(url.query)
        header =  query_params.get("pg", [""])[0]


def randomiseUserAgent():
    global header
    print('Changing the UserAgent now ! Getting new Values !')
    header=  UserAgent().random

def rotateIp():
    # header= randomiseUserAgent()
    print('Changing the Ip now ! Getting new Values !')
    with Controller.from_port(address='tor-privoxy',port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

    

def initBrowserDriver():
    rotateIp()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-proxy-certificate-handler")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        options=options,
        seleniumwire_options=tor_options,
    )
    driver.request_interceptor = interceptor
    return driver

def getMetaData(webdriver):
    listElem =  webdriver.find_elements(by=By.CLASS_NAME,value="LrzXr kno-fv wHYlTd z8gr9e")
    print(listElem)




driver = initBrowserDriver()

# Start
def start(link):
    driver.get(link)
    print("Searching For The Book - "+driver.title )
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
        driver.switch_to.frame(frame)
        print("Switched to frame successfully")
        test_block = len(driver.find_elements(by=By.XPATH,value="/html/body/div[1]/table")) > 0 
        if(test_block):
            print("Google recognized automatic access , Retrying in 5 seconds")
            return      
        for _ in range(5):
            try:     
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'overflow-scrolling')))
                break
            except:
                print("Waiting For Data To Load")
                pass
        print("File finally Loaded successfully")
        time.sleep(10)
        driver.set_script_timeout(90)
        print("Started script execution")
        result = driver.execute_async_script('''
             var callback_final = arguments[arguments.length - 1];
            let book = document.getElementById("viewport");
            let observer = null;
            let targets = [];
            let links = [];
            let scroll = document.getElementsByClassName("overflow-scrolling");
            let scrollHeight = scroll[0].scrollHeight;
            let scrollCount = 0;
            let scrollAmount = 800;
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
                    scrollCount += scrollAmount;
                     if(scrollCount < scrollHeight){
                        scroll[0].scrollBy(0,scrollAmount);
                    }
                    else{
                        callback_final(links)
                        clearInterval(scrollInterval);
                        
                    }
            }
                              
            observer = new MutationObserver(callback);
            observer.observe(book, {
                attributes: true,
                childList: true,
                subtree: true,
            });          
             scrollInterval = 500;
            setInterval(movePage, scrollInterval); 
                                                  
        ''')
        try:
            for link in result:
                pg = extract_pages(link)
                if pg is not None and pg not in pages:
                    pages.append(pg)
                    extracted_links.add(link)
                    new_links.add(link)
        except(e):
            print("can not load the pages , :") 
        
        updateImages()
            
                

    except(Exception) as e:
        print("Error happend when scraping using this ip , Retrying in seconds")
        print(e)
        return
    



def main():
    global link , name
    link = input('Provide the Link for Google Books Book to Scrape: ')
    name = input("Please provide the name of the Book")
    while True:
        start(link)
        # downloadResources(extractedLinks)
        # updateLevel()
        rotateIp()



if(__name__=='__main__'):
    main()
