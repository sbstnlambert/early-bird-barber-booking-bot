# Early Bird Barber Booking Bot

The Early Bird Barber Booking Bot is an automation tool designed to simplify the process of checking for available slots at a hair salon by accessing its online calendar. It provides advanced notifications for appointment cancellations, enabling you to secure your desired time slot with ease. Say goodbye to manual appointment checks and embrace a stress-free scheduling experience!

# Aim of the app

The Early Bird Barber Booking Bot is a small program I created to explore the world of Python programming while solving a practical problem: booking barber appointments online! Please note that this application is specifically tailored to work with a particular barber website based in Belgium. The intricacies of web scraping code are heavily dependent on the structure and content of the website being accessed. As a result, the code provided in this repository is customized for the layout and elements of the specified barber website in Belgium.

Before deploying this application for use, ensure that you have the necessary permissions from the website owner to access and scrape their data. Additionally, be aware that any changes made to the target website's structure or content may require corresponding adjustments to the scraping code in this application.

## Features

- **Automated Slot Checking**: The bot automatically monitors the salon's online calendar for available slots, eliminating the need for manual checks.

- **Advanced Notifications**: Receive notifications in advance when appointment cancellations occur, ensuring you're among the first to book coveted time slots.

## Getting Started

To use the Early Bird Barber Booking Bot, follow these steps:

### Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python**: Make sure you have Python installed on your system. If not, you can download and install Python from [python.org](https://www.python.org/downloads/).

### Installation

1. Clone this repository to your local machine:

```git clone https://github.com/sbstnlambert/early-bird-barber-booking-bot.git```


2. Navigate to the project directory:

```cd early-bird-barber-booking-bot```


3. Install the required Python packages:

```pip install -r requirements.txt```


### Configuration

4. Configure the ChromeDriver path in `config/config.py`, depending on the OS you're using. If the ChromeDriver version doesn't match your Chrome version, find and download the relevant version on the [Google Chrome Labs](https://googlechromelabs.github.io/chrome-for-testing/).

5. Obtain a Pushbullet API key from [Pushbullet](https://www.pushbullet.com/) and update it in `main.py`.

6. Still in `main.py`, select your `appointment_date` in the `check_appointment_availability()` method.

7. Run the bot by executing:

```python main.py```

## Usage

- Upon execution, the bot will launch a Chrome browser and begin checking for available slots based on your configured settings.

- You will receive notifications whenever an appointment cancellation occurs, allowing you to promptly secure your preferred time slot.

## Acknowledgments

Special thanks to the [Pushbullet](https://www.pushbullet.com/) team for their notification service, which enhances the functionality of this bot.

Happy booking!

