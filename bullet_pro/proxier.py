#from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
from selenium import webdriver
from selenium.webdriver.chrome.options import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time

''''------------------------------------
https://www.scrapehero.com/how-to-rotate-proxies-and-ip-addresses-using-python-3/
https://www.pythongasm.com/web-scraping-without-getting-blocked/
https://medium.com/analytics-vidhya/the-art-of-not-getting-blocked-how-i-used-selenium-python-to-scrape-facebook-and-tiktok-fd6b31dbe85f
'''








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

pd.get('https://lichess.org/')


# --- YOU ONLY NEED TO CARE FROM THIS LINE ---
# creating new driver to use proxy


# code must be in a while loop with a try to keep trying with different proxies


# while running:
#     try:
#         pd.get('https://www.expressvpn.com/what-is-my-ip')
        
#         # if statement to terminate loop if code working properly
        
        
#         # you 
#     except:
#         new = ALL_PROXIES.pop()
        
#         # reassign driver if fail to switch proxy
#         pd = proxy_driver(ALL_PROXIES)
#         print("--- Switched proxy to: %s" % new)
#         time.sleep(1)