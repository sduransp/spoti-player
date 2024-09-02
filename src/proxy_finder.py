# Importing libraries
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

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
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--incognito")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=options)

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
        time.sleep(3)  # Wait for the table to reload

        # Find all rows in the table
        rows = self.driver.find_elements(By.XPATH, "//table/tbody/tr[contains(@class, 'spy1x') or contains(@class, 'spy1xx')]")

        for row in rows:
            # Extract the country value
            country_element = row.find_element(By.XPATH, "td[4]")
            country_name = country_element.text.strip()

            if self.country.lower() in country_name.lower():
                # Extract the proxy value (IP:Port)
                proxy_element = row.find_element(By.XPATH, "td[1]")
                proxy_text = proxy_element.text.split("<script")[0].strip()  # Ignore script in the IP field
                print(f"Proxy found for {self.country}: {proxy_text}")
                self.close_browser()
                return proxy_text

        print(f"No proxy found for {self.country}.")
        self.close_browser()
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