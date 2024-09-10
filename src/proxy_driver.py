from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def abrir_chrome_con_proxy(proxy_ip):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-first-run")
    options.add_argument("--incognito")
    options.add_argument("--start-maximized")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument(f'--proxy-server={proxy_ip}')
    
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.whatismyip.com/')  
    time.sleep(50000)

if __name__ == "__main__":
    proxy_ip = '204.44.69.89:6342'

    abrir_chrome_con_proxy(proxy_ip)