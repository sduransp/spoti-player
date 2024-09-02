# Importing libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import random

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
    def __init__(self, username:str, useGUI:bool = False, proxy:str=None, proxy_user:str=None, proxy_pass:str=None,):
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
    
    def send_keys_slowly(self, element, text):
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.15, 0.4))
    
    def login(self):
        """
            Logs into Spotify using the provided username and password.
        """
        self.driver.get(r"https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fopen.spotify.com%2F")
        wait_duration = random.uniform(1, 4) 
        time.sleep(wait_duration)  # Espera a que cargue la página

        # Locating and filling username field
        username_field = self.driver.find_element(By.ID, "login-username")
        self.send_keys_slowly(username_field, self.username)
        wait_duration = random.uniform(1.5, 5)  # Tiempo de espera para emular comportamiento humano
        time.sleep(wait_duration)

        # Locating and filling password field
        password_field = self.driver.find_element(By.ID, "login-password")
        self.send_keys_slowly(password_field, self.password)
        wait_duration = random.uniform(1.5, 5)  # Tiempo de espera para emular comportamiento humano
        time.sleep(wait_duration)

        # Clicking button
        self.driver.find_element(By.ID, "login-button").click()
        wait_duration = random.uniform(1.5, 3)  # Tiempo de espera para emular comportamiento humano
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
        wait_duration = random.uniform(1.5, 3) # Adding a waiting time to emulate human behaviour
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
            wait_duration = random.uniform(2, 5) # Adding a waiting time to emulate human behaviour
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
    bot = SpotifyBot(username="andres.ramajo1995@gmx.com", useGUI=True, proxy="177.93.33.122:999")
    bot.run()