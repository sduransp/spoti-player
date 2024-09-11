import yaml
import threading
import time
import argparse
from datetime import datetime
import pytz
import os
import random
from src.spotify import SpotifyBot  #
import pyautogui

# SETTING GLOBAL VARIABLES
# ------------------------
# Track accounts used each day
used_accounts_today = set()
# Track the current day to reset account usage
current_day = datetime.now().date()
# Global variable for checking whether any thread is paused
is_paused = False
# Lock for handling concurrency
pause_lock = threading.RLock()

def load_accounts(yaml_file_path=None):
    """
    Load Spotify accounts from a YAML configuration file.

    Args:
    yaml_file_path (str): The path to the YAML file containing account information.
                          If not provided, defaults to './config/accounts.yaml'.

    Returns:
    list: A list of accounts, each containing account details such as username, proxy, etc.
    """
    if yaml_file_path is None:
        yaml_file_path = os.path.join(os.path.dirname(__file__), 'config', 'accounts.yaml')

    with open(yaml_file_path, 'r') as file:
        data = yaml.safe_load(file)
    
    return data['accounts']

def filter_accounts_by_time(accounts):
    """
    Filters Spotify accounts based on their local time zone to ensure valid activity times,
    excluding accounts already used today.

    Args:
    accounts (list): List of accounts to be filtered.

    Returns:
    list: A list of valid accounts that can be used at the current time and have not been used today.
    """
    global current_day, used_accounts_today
    valid_accounts = []

    # Reset account usage when a new day starts
    if datetime.now().date() != current_day:
        current_day = datetime.now().date()
        used_accounts_today.clear()

    for account in accounts:
        city = account['city']
        country = account['country']
        username = account['username']

        # Skip accounts that have been used today
        if username in used_accounts_today:
            continue

        # Determine if the current local time allows account usage
        try:
            timezone = pytz.timezone(country)  # Use the first time zone for the country
            local_time = datetime.now(timezone).time()

            # Allowed usage time: 10:00 AM - 11:00 PM
            if datetime.strptime('01:00', '%H:%M').time() <= local_time <= datetime.strptime('23:00', '%H:%M').time():
                valid_accounts.append(account)
        except Exception as e:
            print(f"Error processing account {username} in {city}, {country}: {e}")

    return valid_accounts

def run_spotify_bot(account):
    """
    Executes the Spotify bot for a given account.

    Args:
    account (dict): A dictionary containing the account information, such as username, proxy, etc.
    """
    global is_paused, pause_lock
    proxy_ip = account['proxy']
    proxy_username = account['proxy_username']
    proxy_password = account['proxy_password']
    username = account['username']

    # Initialize and run the Spotify bot
    bot = SpotifyBot(
        username=username,
        useGUI=True,
        proxy=proxy_ip,
        proxy_username=proxy_username,
        proxy_password=proxy_password,
        pause_lock=pause_lock,  
        is_paused=is_paused     
    )
    bot.run()

    # Mark the account as used for today
    used_accounts_today.add(username)

def manage_threads(yaml_file_path, n_threads):
    """
    Manages the execution of multiple Spotify bot threads, ensuring N active listeners at any given time.

    Args:
    yaml_file_path (str): The path to the YAML file containing account information.
    n_threads (int): The number of threads (listeners) to run simultaneously.
    """
    global is_paused, pause_lock
    display_logo()

    accounts = load_accounts(yaml_file_path)
    threads = []

    while True:
        # Filter accounts based on time and usage
        valid_accounts = filter_accounts_by_time(accounts)

        # Launch threads until N active threads are reached
        while len(threads) < n_threads and valid_accounts:
            account = valid_accounts.pop(0)
            thread = threading.Thread(target=run_spotify_bot, args=(account,))
            threads.append(thread)
            threads[-1].start()
            print(f"Initiated account: {account}")
            wait_duration = random.uniform(60, 120)
            time.sleep(wait_duration)
            
        # Check the status of existing threads
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)

        # If not enough valid accounts, wait for 5 minutes before trying again
        if len(threads) < n_threads and not valid_accounts:
            print("Waiting for valid accounts...")
            time.sleep(300)  # Wait 5 minutes

        # Random delay to check thread statuses periodically
        wait_duration = random.uniform(8, 14)
        time.sleep(wait_duration)

def display_logo():
    logo = """

    
    SSSSSSSSSSSSSSS PPPPPPPPPPPPPPPPP   OOOOOOOOO     TTTTTTTTTTTTTTTTTTTTTTT  IIIIIIIIIIII
  SS:::::::::::::::SP::::::::::::::::P O:::::::O     T:::::::::::::::::::::T   I::::::::::I
 S:::::SSSSSS::::::SP::::::PPPPPP:::::PO:::::::O     T:::::::::::::::::::::T   I::::::::::I
 S:::::S     SSSSSSSPP:::::P     P:::::PO:::::::O     T:::::TT:::::::TT:::::T  I::::::::::I
 S:::::S              P::::P     P:::::PO:::::O O::::O TTTTTT  T:::::T  TTTTTT I::::::::::I
 S:::::S              P::::P     P:::::PO:::::O O::::O         T:::::T         I::::::::::I
  S::::SSSS           P::::PPPPPP:::::P O:::::O O::::O         T:::::T         I::::::::::I
   SS::::::SSSSS      P:::::::::::::PP  O:::::O O::::O         T:::::T         I::::::::::I
     SSS::::::::SS    P::::PPPPPPPPP    O:::::O O::::O         T:::::T         I::::::::::I
        SSSSSS::::S   P::::P            O:::::O O::::O         T:::::T         I::::::::::I
             S:::::S  P::::P            O:::::O O::::O         T:::::T         I::::::::::I
             S:::::S  P::::P            O::::::O::::::O        T:::::T         I::::::::::I
 SSSSSSS     S:::::SPP::::::PP          O:::::::::::::O      TT:::::::TT       I::::::::::I 
 S::::::SSSSSS:::::SP::::::::P           OO:::::::::OO       T:::::::::T       I::::::::::I 
 S:::::::::::::::SS P::::::::P             OOOOOOOOO         T:::::::::T       I::::::::::I 
  SSSSSSSSSSSSSSS   PPPPPPPPPP                               TTTTTTTTTTT       I::::::::::I


    H:::::::H     H:::::::H       A:::::A       CCCCCCCCCCCCCK    KKKKKKKK    KKKKKKK
    H:::::::H     H:::::::H      A:::::::A    CCC::::::::::::C   K:::::::K    K:::::K
    H:::::::H     H:::::::H     A:::::::::A  CC:::::::::::::::K   :::::::K    K:::::K
    HH::::::H     H::::::HH    A:::::A:::::AC:::::CCCCCCCC::::KK   ::::::K    K:::::K
      H:::::H     H:::::H     A:::::A A::::AC:::::C       CCCCCC    K:::::K K:::::K  
      H:::::H     H:::::H    A:::::A   A::::AC:::::C                 K::::::K:::::K 
      H::::::HHHHH::::::H   A:::::A     A::::AC:::::C                 K:::::::::::K 
      H:::::::::::::::::H  A:::::AAAAAAAAA:::::AC:::::C               K:::::::::::K
      H:::::::::::::::::H A:::::::::::::::::::::AC:::::C               K::::::K:::::K 
      H::::::HHHHH::::::HA:::::AAAAAAAAAAAAA:::::AC:::::C               K::::::K K:::::K
      H:::::H     H:::::H:::::A               A:::::AC:::::C       CCCCCC K:::::K  K:::::K
      H:::::H     H:::::H:::::A                 A:::::AC:::::CCCCCCCC::: :KK::::::K   K::::::K
    HH::::::H     H:::::H:::::A                   A:::::AC::::::::::::::: CK:::::::K    K:::::K
    H:::::::H     H:::::::A                             CCC::::::::::::CK    :::::::K    K:::::K
    H:::::::H     H:::::A                               CCC::::::::::CK      :::::::K    K:::::K
               

    """
    print(logo)

if __name__ == "__main__":
    # Command-line argument parsing to specify YAML file and number of threads
    parser = argparse.ArgumentParser(description="Script to execute Spotify bots across multiple accounts.")
    parser.add_argument('--yaml_file', type=str, default='config/accounts.yaml', help='Path to the YAML file containing account information')
    parser.add_argument('--threads', type=int, default=3, help='Number of simultaneous bot threads')

    args = parser.parse_args()

    # Run the thread management with the specified number of threads
    manage_threads(args.yaml_file, args.threads)