# Early Bird Barber Booking Bot

The Early Bird Barber Booking Bot is an automation tool designed to simplify the process of checking for available slots at a hair salon by accessing its online calendar. It provides advanced notifications for appointment cancellations, enabling you to secure your desired time slot with ease. Say goodbye to manual appointment checks and embrace a stress-free scheduling experience!

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

4. Configure the bot settings in `config/config.py`, including the salon's URL and ChromeDriver path.

5. Obtain a Pushbullet API key from [Pushbullet](https://www.pushbullet.com/) and update it in the `Notifier` class constructor in `notifications/notifier.py`.

6. Run the bot by executing:

```python main.py```

## Usage

- Upon execution, the bot will launch a Chrome browser and begin checking for available slots based on your configured settings.

- You will receive notifications whenever an appointment cancellation occurs, allowing you to promptly secure your preferred time slot.

## Acknowledgments

Special thanks to the [Pushbullet](https://www.pushbullet.com/) team for their notification service, which enhances the functionality of this bot.

Happy booking!

