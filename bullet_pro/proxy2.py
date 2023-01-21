from selenium import webdriver
from selenium.webdriver.chrome.options import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from stockfish import Stockfish
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import chess
import chess.engine
import random
from fake_useragent import UserAgent

''''------------------------------------
https://www.scrapehero.com/how-to-rotate-proxies-and-ip-addresses-using-python-3/
https://www.pythongasm.com/web-scraping-without-getting-blocked/
https://medium.com/analytics-vidhya/the-art-of-not-getting-blocked-how-i-used-selenium-python-to-scrape-facebook-and-tiktok-fd6b31dbe85f
'''
stockfish = Stockfish(r'C:\Users\user\Desktop\problemler\bullet_pro\stockfish_13_win_x64_ssse\stockfish_13_win_x64_ssse.exe')
engine = chess.engine.SimpleEngine.popen_uci(r'C:\Users\user\Desktop\problemler\bullet_pro\stockfish_13_win_x64_ssse\stockfish_13_win_x64_ssse.exe')
board = chess.Board()

def login(driver):
    driver.get("https://lichess.org/login?referrer=/")

    user=driver.find_element_by_name("username")
    user.send_keys("") #username
    passw=driver.find_element_by_name("password")
    passw.send_keys("") #pass
    login=driver.find_element(By.XPATH,'//*[@id="main-wrap"]/main/form/div[1]/button').click()

time.sleep(1)
#wait = WebDriverWait(driver, 10)

def drop(mylist, n):
    del mylist[0::n]
    return (mylist)

def get_notation():
    try:
        #wait = WebDriverWait(driver, 10)
        #nots1=driver.find_element(By.CSS_SELECTOR,'l4x')
        nots1=WebDriverWait(pd,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'l4x')))
        nots_list1=nots1.text.split()
    except:
        time.sleep(1)
        get_notation()
    return drop(nots_list1,3)

def play_algo(driver):
    try:
        notas=get_notation()
        board = chess.Board()
        while not board.is_game_over():
            for i in range(len(notas)):
                board.push_san(notas[i])
            

            result = engine.play(board, chess.engine.Limit(depth=10))
            board.push(result.move)
            a=result.move
            blindkey=driver.find_element(By.XPATH,'//*[@id="main-wrap"]/main/div[1]/div[10]/input')
            blindkey.send_keys(str(a)+Keys.RETURN)
            blindkey.clear()
            board=chess.Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
            notas=get_notation()
            if 10<len(notas)<30:
                time.sleep(random.randrange(0,3000)/1000)
            else:
                pass
    except:
        time.sleep(1)
        play_algo(driver=pd)
        #time.sleep(1)






#------------------------
executable_path= r"C:\Program Files (x86)\chromedriver.exe"

co = webdriver.ChromeOptions()
co.add_argument("log-level=3")
#co.add_argument("--headless")

def get_proxies(co=co):
    
    driver = webdriver.Chrome(executable_path= r"C:\Program Files (x86)\chromedriver.exe",chrome_options=co)
    driver.get("https://free-proxy-list.net/")

    PROXIES = []
    proxies = driver.find_elements_by_css_selector("tr[role='row']")
    for p in proxies:
        result = p.text.split(" ")

        if result[-1] == "yes":
            PROXIES.append(result[0]+":"+result[1])

    driver.close()
    return PROXIES


ALL_PROXIES = get_proxies()
print(ALL_PROXIES)

def proxy_driver(PROXIES, co=co):
    prox = Proxy()

    if len(PROXIES) < 1:
        print("--- Proxies used up (%s)" % len(PROXIES))
        PROXIES = get_proxies()
        
    pxy = PROXIES[-1]

    prox.proxy_type = ProxyType.MANUAL
    prox.http_proxy = pxy
    #prox.socks_proxy = pxy
    prox.ssl_proxy = pxy

    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)

    driver = webdriver.Chrome(executable_path= r"C:\Program Files (x86)\chromedriver.exe",options=co, desired_capabilities=capabilities)

    return driver

pd = proxy_driver(ALL_PROXIES)

#pd.get('https://lichess.org/')

# login(driver=pd)
# play_algo(driver=pd)

running=True
while running:
    try:
        login(driver=pd)
        play_algo(driver=pd)

        if len(ALL_PROXIES)==0:
            running=False
        # if statement to terminate loop if code working properly
        
        
        # you 
    except:
        new = ALL_PROXIES.pop()
        
        # reassign driver if fail to switch proxy
        pd = proxy_driver(ALL_PROXIES)
        print("--- Switched proxy to: %s" % new)
        time.sleep(1)