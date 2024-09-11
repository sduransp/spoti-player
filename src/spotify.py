# Importing libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import random
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
    def __init__(self, username:str, useGUI:bool = False, proxy:str=None, proxy_username:str=None, proxy_password:str=None,pause_lock=None, is_paused=None):
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
        self.pause_lock = pause_lock  
        self.is_paused = is_paused   
        self.driver = None
        self.album_file = os.path.join(os.path.dirname(__file__), '../config/albums.yaml')
        self.primary_album = None
        self.alternate_albums = []

        self.load_albums()

    def load_albums(self):
        """
        Loads the album URLs from a YAML file.
        """
        with open(self.album_file, 'r') as file:
            data = yaml.safe_load(file)
            self.primary_album = data['albums']['primary']
            self.alternate_albums = data['albums']['alternates']
    
    def choose_album(self):
        """
        Chooses an album to navigate to based on an 80% probability of selecting the primary album,
        and 20% for an alternate album.
        """
        if random.random() < 0.8:  
            return self.primary_album
        else:  
            return random.choice(self.alternate_albums)
    
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
                if char == '@':  
                    pyautogui.keyDown('alt')
                    pyautogui.press('2')    
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
        wait_duration = random.uniform(1, 2) 
        time.sleep(wait_duration)

        # enter credentials
        self.send_keys_slowly(text=self.proxy_username)
        wait_duration = random.uniform(1.5, 3) 
        time.sleep(wait_duration)

        self.send_keys_slowly(text=self.proxy_password, last=True)
        wait_duration = random.uniform(1, 3)  
        time.sleep(wait_duration)

        # Locating and filling username field
        username_field = self.driver.find_element(By.ID, "login-username")
        self.send_keys_slowly(username_field, self.username)
        wait_duration = random.uniform(1.5, 3)  # Tiempo de espera para emular comportamiento humano
        time.sleep(wait_duration)

        # Locating and filling password field
        password_field = self.driver.find_element(By.ID, "login-password")
        self.send_keys_slowly(password_field, self.password)
        wait_duration = random.uniform(1.5, 3) 
        time.sleep(wait_duration)

        # Clicking button
        self.driver.find_element(By.ID, "login-button").click()
        wait_duration = random.uniform(1.5, 2)  
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
        wait_duration = random.uniform(1.5, 2.2) 
        time.sleep(wait_duration)
    
    def get_mouse_position(self):
        try:
            while True:
                
                x, y = pyautogui.position()
                print(f"Posición del ratón: X={x} Y={y}", end="\r")  
                time.sleep(0.1)  
        except KeyboardInterrupt:
            print("\nFinalizado.")

    def start_playback(self):
        """
        Locates and clicks the play button on the album page, forcing the click using JavaScript.
        Prepares the initial playback setup.
        """
        try:
            # Locate the play button using its CSS selector
            play_button = self.driver.find_element(By.CSS_SELECTOR, 'button.j2s64Lz8y6VzBLB_V9Gm')

            # Scroll to the play button to ensure it's in view
            wait_duration = random.uniform(1.2, 3)
            time.sleep(wait_duration)

            # Force a click on the play button using JavaScript
            self.driver.execute_script("arguments[0].click();", play_button)
            print("Play button clicked using JavaScript.")

            # Initial setup: clicking on the required areas using pyautogui
            pyautogui.click(x=961, y=429)
            wait_duration = random.uniform(0.5, 0.9)
            time.sleep(wait_duration)
            pyautogui.click(x=1136, y=824)
            wait_duration = random.uniform(0.5, 0.9)
            time.sleep(wait_duration)
            pyautogui.click(x=106, y=811)
            wait_duration = random.uniform(0.5, 0.9)
            time.sleep(wait_duration)

            # Return album duration and pause probability threshold
            album_duration = random.randint(1800, 1830)
            pause_probability_threshold = random.randint(133, 322)  # Probability threshold for pausing the playback

            return album_duration, pause_probability_threshold

        except Exception as e:
            print(f"Could not find or click the play button: {e}")
    
    def simulate_playback(self, album_duration, pause_probability_threshold):
        """
        Simulates listening to the album, randomly pausing and resuming the playback.
        Includes the main playback loop.
        """
        elapsed_time = 0
        checked_play_pause = False
        clicked_next_previous = False

        try:
            while elapsed_time < album_duration:
                start_time = time.time()

                # Estimating the probability of pausing
                random_pause_chance = random.randint(1, 100000)
                if random_pause_chance < pause_probability_threshold:
                    with self.pause_lock:
                        if not self.is_paused:
                            self.is_paused = True
                            self.driver.execute_script("window.focus();")
                            pause_duration = random.uniform(1, 35)
                            self.pause_song(pause_duration)
                            self.is_paused = False

                # Check if play/pause button is "Pause" (indicating music is playing) between seconds 3 and 5
                if 3 <= elapsed_time % 10 <= 5 and not checked_play_pause:
                    try:
                        play_pause_button = self.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="control-button-playpause"]')
                        play_pause_status = play_pause_button.get_attribute("aria-label")

                        if play_pause_status == "Play":
                            print("Music is paused, clicking play.")
                            play_pause_button.click()
                        else:
                            print("Music is playing.")

                        checked_play_pause = True  # Ensure this block is entered only once per cycle

                    except Exception as e:
                        print(f"Could not find play/pause button: {e}")

                # Press "Next" button between seconds 6 and 8
                if 6 <= elapsed_time % 10 <= 8 and not clicked_next_previous:
                    try:
                        next_button = self.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="control-button-skip-forward"]')
                        next_button.click()
                        print("Clicked 'Next' button.")

                        wait_duration = random.uniform(0.8, 1.5)
                        time.sleep(wait_duration)

                        previous_button = self.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="control-button-skip-back"]')
                        previous_button.click()
                        print("Clicked 'Previous' button.")

                        clicked_next_previous = True  # Ensure this block is entered only once per cycle

                    except Exception as e:
                        print(f"Error clicking next/previous button: {e}")

                # Calculate the actual time spent in the loop
                loop_duration = time.time() - start_time
                if loop_duration < 1:
                    time.sleep(1 - loop_duration)
                    elapsed_time += 1
                else:
                    elapsed_time += loop_duration

        except Exception as e:
            print(f"Error during playback: {e}")

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
        while True:  
            print(f"Trying to run account - paused lock: {self.is_paused}")
            with self.pause_lock:
                if not self.is_paused:
                    self.is_paused = True 
                    print(f"Lock activated: {self.is_paused}")
                    self.setup_browser()
                    print("Browser setup")
                    self.login()
                    print(f"Logged in")
                    album_url = self.choose_album()
                    print(f"Album selected: {album_url}")
                    self.navigate_to_album(album_url)
                    print(f"About to start playing album")
                    album_duration, pause_probability_threshold = self.start_playback()
                    break  
                else:
                    print("El bot está en pausa, esperando 15 segundos antes de reintentar...")
            
            time.sleep(15)
        self.simulate_playback(album_duration, pause_probability_threshold)
        self.close_browser()
