# Importing libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import random
from proxy_finder import ProxyFinder
import pyautogui
import yaml

# Adding functionality
class SpotifyBot:
    """
        A bot to automate interactions with Spotify, such as logging in, navigating to an album, and playing it.
        
        Attributes:
        -----------
        username : str
            Spotify username or email address used to log in.
        password : str
            Spotify password retrieved from the environment variable 'spotify-password'.
        driver : webdriver.Chrome
            Selenium WebDriver instance used to interact with the browser.
    """
    def __init__(self, username:str, useGUI:bool = False, proxy:str=None, proxy_username:str=None, proxy_password:str=None,):
        """
            Initializes the SpotifyBot with a username and retrieves the password from the environment.
            
            Parameters:
            -----------
            username : str
                The Spotify username or email address.
            useGUI : bool
                Option to enable displaying the GUI
            proxy : str
                The proxy address in the format 'ip:port'.
            proxy_user : str, optional
                The username for proxy authentication (if required).
            proxy_pass : str, optional
                The password for proxy authentication (if required).
        """
        self.username = username
        self.password = os.getenv('SPOTIFY_PASSWORD')
        self.useGUI = useGUI
        self.proxy_ip = proxy
        self.proxy_username = proxy_username
        self.proxy_password = proxy_password
        self.driver = None
    
    def setup_browser(self):
        """
        Sets up the Selenium WebDriver with Chrome options and initializes the browser instance.
        """
        options = webdriver.ChromeOptions()
        if not self.useGUI:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-first-run")
        options.add_argument("--incognito")
        options.add_argument("--start-maximized")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument(f"--proxy-server={self.proxy_ip}")

        self.driver = webdriver.Chrome(options=options)
        
    
    def send_keys_slowly(self, element=None, text=None, last=False):
        if element:
            for char in text:
                element.send_keys(char)
                time.sleep(random.uniform(0.15, 0.4))
        else:
            # Usar pyautogui para enviar el texto en la posición actual del cursor
            for char in text:
                if char == '@':  # Detecta si es un @ y usa la combinación Shift + 2 en Mac
                    pyautogui.keyDown('alt')  # Mantén presionada la tecla Option (Alt)
                    pyautogui.press('2')       # Presiona la tecla 2
                    pyautogui.keyUp('alt')
                else:
                    pyautogui.write(char)
                time.sleep(random.uniform(0.15, 0.4))
            
            if last:
                pyautogui.press('enter')
            else:
                pyautogui.press('tab')

    
    def login(self):
        """
            Logs into Spotify using the provided username and password.
        """
        self.driver.get(r"https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fopen.spotify.com%2F")
        wait_duration = random.uniform(2, 4) 
        time.sleep(wait_duration)

        # enter credentials
        self.send_keys_slowly(text=self.proxy_username)
        wait_duration = random.uniform(1.5, 5) 
        time.sleep(wait_duration)

        self.send_keys_slowly(text=self.proxy_password, last=True)
        wait_duration = random.uniform(5, 10)  
        time.sleep(wait_duration)

        # Locating and filling username field
        username_field = self.driver.find_element(By.ID, "login-username")
        self.send_keys_slowly(username_field, self.username)
        wait_duration = random.uniform(1.5, 5)  # Tiempo de espera para emular comportamiento humano
        time.sleep(wait_duration)

        # Locating and filling password field
        password_field = self.driver.find_element(By.ID, "login-password")
        self.send_keys_slowly(password_field, self.password)
        wait_duration = random.uniform(1.5, 5) 
        time.sleep(wait_duration)

        # Clicking button
        self.driver.find_element(By.ID, "login-button").click()
        wait_duration = random.uniform(1.5, 3)  
        time.sleep(wait_duration)
    
    def navigate_to_album(self, album_url):
        """
            Navigates to a specified album page on Spotify.

            Parameters:
            -----------
            album_url : str
                The URL of the album to navigate to.
        """
        self.driver.get(album_url)
        wait_duration = random.uniform(1.5, 3) 
        time.sleep(wait_duration)

    def play_album(self):
        """
        Locates and clicks the play button on the album page, forcing the click using JavaScript.
        Then, it simulates listening to the album, randomly pausing and resuming the playback.
        """
        try:
            # Locate the play button using its CSS selector
            play_button = self.driver.find_element(By.CSS_SELECTOR, 'button.j2s64Lz8y6VzBLB_V9Gm')

            # Scroll to the play button to ensure it's in view
            wait_duration = random.uniform(2, 5) 
            time.sleep(wait_duration)

            # Force a click on the play button using JavaScript
            self.driver.execute_script("arguments[0].click();", play_button)
            print("Play button clicked using JavaScript.")

            # Simulate listening to the album with random pauses
            album_duration = random.randint(1800, 1830)
            elapsed_time = 0
            pause_probability_threshold = random.randint(133, 322)  # Probability threshold for pausing the playback (adjust as needed)
            
            while elapsed_time < album_duration:
                random_pause_chance = random.randint(1, 100000)

                if random_pause_chance < pause_probability_threshold:
                    pause_duration = random.uniform(1, 35)  # Random pause duration between 1 and 35 seconds
                    self.pause_song(pause_duration)

                time.sleep(1)  # Wait for 1 second to simulate playback
                elapsed_time += 1

        except Exception as e:
            print(f"Could not find or click the play button: {e}")

    def pause_song(self, duration):
        """
        Pauses the song for a given duration and then resumes playback.

        Parameters:
        -----------
        duration : float
            The amount of time to pause the playback, in seconds.
        """
        try:
            # Simulate pausing the song (implement the actual pause logic here if needed)
            overhead_pause = random.uniform(1.5, 2.5) 
            time.sleep(overhead_pause)
            print(f"Pausing song for {duration:.2f} seconds.")

            # Clicking pause button
            pause_button = self.driver.find_element(By.CSS_SELECTOR, 'button.j2s64Lz8y6VzBLB_V9Gm')
            self.driver.execute_script("arguments[0].click();", pause_button)

            # Waiting for the pause duration
            time.sleep(duration) 

            # Clicking resume button
            self.driver.execute_script("arguments[0].click();", pause_button)
            print("Resuming song playback.")

        except Exception as e:
            print(f"Error during pause: {e}")
    

    def close_browser(self):
        """
            Closes the browser instance.
        """
        self.driver.quit()
    def run(self):
        """
            Runs the complete bot process: setting up the browser, logging in, navigating to an album, playing it, and closing the browser.
        """
        self.setup_browser()
        self.login()
        self.navigate_to_album(r"https://open.spotify.com/album/4lJ0vy0SIlMxHYofabpjng")
        self.play_album()
        self.close_browser()

if __name__ == "__main__":


    # Obtener la ruta del archivo YAML usando ruta relativa
    yaml_file_path = os.path.join(os.path.dirname(__file__), '../config/accounts.yaml')

    # Cargar el archivo YAML
    with open(yaml_file_path, 'r') as file:
        data = yaml.safe_load(file)

    # Test cuenta 1:
    username = data["accounts"][0]["username"]
    country = data["accounts"][0]["country"]
    proxy_ip = data["accounts"][0]["proxy"]
    proxy_username = data["accounts"][0]["proxy_username"]
    proxy_password = data["accounts"][0]["proxy_password"]

    finder= ProxyFinder(country=country)
    proxy = finder.find_proxy()
    bot = SpotifyBot(username=username, useGUI=True, proxy=proxy_ip, proxy_username=proxy_username,proxy_password=proxy_password)
    bot.run()