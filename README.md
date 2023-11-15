## Overview

This Python program is designed to track the availability of classes at the University of South Florida (USF) and notify users when there are changes in the class status, such as openings for registration. The program uses web scraping techniques to extract class information from the USF online class schedule.

## Features

- **Menu Interface**: The program provides a simple menu interface with options to start the class monitoring process or exit the program.

- **Class Monitoring**: The main functionality of the program involves continuously monitoring the availability of specified classes. It uses a configuration file (`config.json`) to define the classes to be monitored, timeouts, and delays between checks.

- **Web Scraping**: The program utilizes the `requests` library and `BeautifulSoup` for web scraping. It simulates form submissions on the USF online class schedule website to retrieve class information.

- **Database Storage**: Class information is stored in an SQLite database (`database.db`). The program checks for changes in class status and updates the database accordingly.

- **Notification**: When changes are detected, the program sends notifications using Discord webhooks. The notifications include details about the class, such as the status, title, instructor, seat capacity, and availability.

## Prerequisites

Before running the program, ensure the following:

- Python is installed on your system.
- Required Python packages are installed. You can install them using the following command:

```sh
pip install -r requirements.txt
```

## Configuration

- The program uses a configuration file (`config.json`) to specify the classes to monitor, timeouts, delays, and Discord webhook information. Ensure this file is correctly configured before running the program.

## Running

```sh
python3 app.py
```

## Disclaimer

This program is specific to the University of South Florida's online class schedule format. Changes to the website structure may affect the program's functionality.


## Acknowledgments

- The program uses the `requests` library, `BeautifulSoup`, and `DiscordWebhook` library. Special thanks to the developers of these libraries for their contributions.
