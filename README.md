## 🎧 Spotify Album Playback Bot with Proxy Support

This project is an educational tool that automates the process of increasing the playback count of a specific Spotify album using multiple accounts and proxies. The bot is capable of logging in to Spotify using different accounts, navigating to the album page, and playing it using Selenium and a proxy to simulate unique user activity.

![logo](https://i0.wp.com/musically.com/wp-content/uploads/2023/05/spotify-logo.jpg?fit=1200%2C762&ssl=1)

🚨 **Disclaimer:** This project is strictly for educational purposes and to explore automation techniques. It should not be used for unethical purposes, such as artificially inflating Spotify streams or violating Spotify’s Terms of Service.

### Features

	•	✅ Automated Spotify Playback: The bot logs in, navigates to a specific album, and plays it automatically.
	•	✅ Multi-threaded Playback: Use multiple Spotify accounts simultaneously, each using a separate proxy to simulate unique users.
	•	✅ Proxy Support: Each bot instance logs in using a different IP address through proxy rotation to avoid detection.
	•	✅ Human-like Interaction: The bot emulates human interaction through randomized delays and actions, making it more realistic.
	•	✅ Configuration via YAML: Account information and proxy details are loaded from a YAML configuration file for easy management.

### How It Works

The bot uses **Selenium WebDriver** to simulate a browser, logs into Spotify, and navigates to the album page to start playback. It uses proxies to log in from different IP addresses to avoid Spotify’s detection systems. The bot can simulate listening to the album for a random amount of time, pausing occasionally to further mimic human behavior.

### Bot Workflow:

	1.	Account Authentication: Logs into Spotify using credentials loaded from a YAML file.
	2.	Proxy Assignment: Each account operates under a different proxy IP to appear as a separate user.
	3.	Album Navigation: The bot automatically navigates to the specified Spotify album URL.
	4.	Simulate Listening: It clicks the “Play” button and simulates listening by keeping the album playing for a randomized duration.
	5.	Human-like Interaction: Includes random pauses and resume actions to mimic real users.

### Requirements

	•	Python 3.10
	•	Selenium WebDriver
	•	Chrome Browser and ChromeDriver
	•	PyYAML (for configuration parsing)
	•	PyAutoGUI (for keystroke automation)
	•	Proxy Finder (for IP rotation)


### Installation

	1.	Clone the repository:

	git clone https://github.com/sduransp/spoti-player.git

	2. Install dependencies - There are also conda dependencies

	conda create --name <environment_name> 
	conda activate <environment_name>
	pip install -r requirements.txt



### Usage

To run the bot with the specified Spotify account and proxy settings from your YAML configuration:

```bash
python run.py -n -p
```

where:

	•	n = number of different account listening simultenously
	•	p = probability of listening the provided album

*There is a probability of listening a different album from a random list, so it intends to mimic human behaviours.
Not always selecting the same album*


### Configuration

Edit the config/accounts.yaml file to manage your Spotify account information and proxy details.

### Important Notes

	•	This bot requires ChromeDriver to be installed and accessible via your system’s PATH.
	•	Ensure you configure proxies carefully to avoid IP bans.
	•	Spotify might detect unusual activity and take action, including banning accounts or blocking IPs.

### Educational Use Only

This project is intended solely for educational purposes to demonstrate automation, proxy handling, and browser control using Selenium. Misuse of this project for unethical purposes is strongly discouraged.

### License

This project is licensed under the MIT License. See the LICENSE file for more details.

With this setup, your repository will clearly describe the project’s purpose, usage, and configuration while emphasizing its educational nature and ethical considerations.