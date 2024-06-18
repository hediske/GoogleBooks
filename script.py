from fake_useragent import UserAgent
from stem.control import Controller
from stem import Signal
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

sys.stderr = open('log.txt', 'w')


from format import CustomFormatter


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




driver = initBrowserDriver()

# Start
def start(link):
    driver.get(link)
    print("Searching For The Book - "+driver.title )
    time.sleep(2.5)
    if(driver.current_url != link):
        print("Google Blocked Access to this ip , Retrying in 5 seconds")
        time.sleep(5)
        return
    # WebDriverWait(driver,5).until(lambda d: d.execute_script('return document.readyState') == 'complete')
    xpath_but = '//*[@id="main"]/div[1]/div[2]/div[1]/div/entity-page-viewport-entry/div'
    # getMetaData(driver)
    while True:
        try:
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,xpath_but))).click()
            print('Clicked on button to advance ! Generating Pages for This IP successfully')
        except Exception as e:
            pass
        try:
            print("loading the document !")
            # WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img[aria-label="Page"]:first-child')))
            WebDriverWait(driver,10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"#s7Z8Jb")))
            print("Changing to the frame ")
            if(len(driver.find_elements(by=By.XPATH,value="/html/body/div[1]/table")) > 0 ):
                print("Google recognized automatic access , Retrying in 5 seconds")
                time.sleep(2.5)
                return           
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img[aria-label="Page"]:first-child')))
            print("File finally Loaded successfully")
            time.sleep(2)
            driver.execute_script('
                console.log("Scraping Started !");
                let scroll = document.getElementsByClassName("overflow-scrolling");
                console.log(scroll);


                let scrollCount = 0;
                let scrollHeight = scroll[0].scrollHeight;
                let scrollCount = 0;
                let scrollAmount = 800;
                let scrollInterval = "" ;


                let movePage = function (){
                    scrollCount += Math.floor( ( scrollAmount - 500 + 1 ) * Math.random()  + 500);
                    if(scrollCount < scrollHeight){
                        scroll[0].scrollBy(0,scrollAmount);
                    }
                    else 
                        clearInterval(scrollInterval);
                }

                                  
                                  ')
            break
        except(Exception) as e:
            print("Error happend when scraping using this ip , Retrying in seconds")
            print(e)
            pass
    



def main():
    # link = input('Provide the Link for Google Books Book to Scrape: ')
    link = 'https://www.google.fr/books/edition/Ace_AWS_Certified_Solutions_Architect_As/2GPiEAAAQBAJ?hl=fr&gbpv=0'
    while(True):
        start(link)
        # downloadResources(extractedLinks)
        # updateLevel()
        rotateIp()



if(__name__=='__main__'):
    main()
