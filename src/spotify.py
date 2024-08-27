# Importing libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
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
    def __init__(self, username:str, useGUI:bool = False):
        """
            Initializes the SpotifyBot with a username and retrieves the password from the environment.
            
            Parameters:
            -----------
            username : str
                The Spotify username or email address.
            useGUI : bool
                Option to enable displaying the GUI
        """
        self.username = username
        self.password = os.getenv('spotify-password')
        self.useGUI = useGUI
        self.driver = None
    
    def setup_browser(self):
        """
            Sets up the Selenium WebDriver with Chrome options and initializes the browser instance.
        """
        options = webdriver.ChromeOptions()
        if not self.useGUI:
            options.add_argument("--headless")  
        options.add_argument("--no-sandbox")  # Recommended for server environments
        options.add_argument("--disable-dev-shm-usage")  # Avoid issues in containerized environments
        self.driver = webdriver.Chrome(options=options)
    
    def login(self):
        """
            Logs into Spotify using the provided username and password.
        """
        self.driver.get(r"https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fopen.spotify.com%2F")
        time.sleep(2)  # Espera a que cargue la página

        # Ingresar credenciales y hacer login
        self.driver.find_element(By.ID, "login-username").send_keys(self.username)
        self.driver.find_element(By.ID, "login-password").send_keys(self.password)
        self.driver.find_element(By.ID, "login-button").click()

        time.sleep(5)
    
    def navigate_to_album(self, album_url):
        """
            Navigates to a specified album page on Spotify.

            Parameters:
            -----------
            album_url : str
                The URL of the album to navigate to.
        """
        self.driver.get(album_url)
        time.sleep(2)
    def play_album(self):
        """
        Locates and clicks the play button on the album page, forcing the click using JavaScript.
        Then, it simulates listening to the album, randomly pausing and resuming the playback.
        """
        try:
            # Locate the play button using its CSS selector
            play_button = self.driver.find_element(By.CSS_SELECTOR, 'button.j2s64Lz8y6VzBLB_V9Gm')

            # Scroll to the play button to ensure it's in view
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", play_button)
            time.sleep(1)

            # Force a click on the play button using JavaScript
            self.driver.execute_script("arguments[0].click();", play_button)
            print("Play button clicked using JavaScript.")

            # Simulate listening to the album with random pauses
            album_duration = 1800  # Total duration to simulate (30 minutes)
            elapsed_time = 0
            pause_probability_threshold = 166  # Probability threshold for pausing the playback (adjust as needed)

            while elapsed_time < album_duration:
                random_pause_chance = random.randint(1, 100000)

                if random_pause_chance < pause_probability_threshold:
                    pause_duration = random.uniform(1, 20)  # Random pause duration between 1 and 20 seconds
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
            print(f"Pausing song for {duration:.2f} seconds.")
            time.sleep(duration)  # Wait for the pause duration

            # Simulate resuming the song (implement the actual resume logic here if needed)
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
    bot = SpotifyBot()
    bot.run()