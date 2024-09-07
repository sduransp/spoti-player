# Importing libraries
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui

# Proxy finder functionality
class ProxyFinder:
    def __init__(self, country:str):
        """
        Initializes the ProxyFinder class.
        
        Parameters:
        -----------
        country : str
            The name of the country to search for in the proxy table.
        """
        self.country = country
        self.driver = None

        self.setup_browser()

    def setup_browser(self):
        """Sets up the Chrome browser with Selenium."""
        self.driver = uc.Chrome(headless=False,use_subprocess=True)
    
    def handle_recaptcha(self, x, y):
        """
        Automates reCAPTCHA by clicking on known coordinates.
        """
        print("Detecting CAPTCHA...")
        try:
            # Esperar 5 segundos antes de hacer clic, puedes ajustar este tiempo
            time.sleep(5)
            
            # Realizar clic en las coordenadas proporcionadas
            print(f"Haciendo clic en las coordenadas X={x}, Y={y}")
            pyautogui.click(x=x, y=y)
            
            # Esperar después de hacer clic, asegurando que se procese la interacción
            time.sleep(1)
            print("reCAPTCHA clic realizado.")

        except Exception as e:
            print(f"Error while solving reCAPTCHA: {str(e)}")

    def find_proxy(self):
        """
        Searches for a proxy in the table based on the provided country.
        
        Returns:
        --------
        str: Proxy address in the format 'IP:Port' if found, otherwise None.
        """
        self.driver.get("https://spys.one/en/free-proxy-list/")
        time.sleep(2)

        # Select the option to show 500 proxies
        select_element = Select(self.driver.find_element(By.ID, "xpp"))
        select_element.select_by_value("5")
        time.sleep(1)  # Wait for the table to reload

        print(f"Assessing whether there is captcha in {self.driver.page_source}")
        if "momento" in self.driver.page_source:
            self.handle_recaptcha(x=307, y=407)
            time.sleep(5)

        # Find all rows in the table
        rows = self.driver.find_elements(By.XPATH, "//table/tbody/tr[contains(@class, 'spy1x') or contains(@class, 'spy1xx')]")

        for row in rows:
            # Extract the country value
            country_element = row.find_element(By.XPATH, "td[4]")
            country_name = country_element.text.strip()

            if self.country.lower() in country_name.lower():
                # Extract the proxy value (IP:Port)
                proxy_element = row.find_element(By.XPATH, "td[1]")
                proxy_text = proxy_element.text.split("<script")[0].strip() 
                print(f"Proxy found for {self.country}: {proxy_text}")
                self.close_browser()
                return proxy_text

        print(f"No proxy found for {self.country}.")
        # self.close_browser()
        return None

    def close_browser(self):
        """Closes the browser."""
        if self.driver:
            self.driver.quit()

# Using the ProxyFinder
if __name__ == "__main__":
    finder = ProxyFinder(country="Brazil")
    proxy = finder.find_proxy()
    
    if proxy:
        print(f"Proxy found: {proxy}")
    else:
        print("No proxy found for the specified country.")