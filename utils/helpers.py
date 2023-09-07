# utils/helpers.py
from pushbullet import Pushbullet

# Create a dictionary mapping month names to their corresponding numerical values.
MONTH_MAP = {
    "janvier": 1,
    "février": 2,
    "mars": 3,
    "avril": 4,
    "mai": 5,
    "juin": 6,
    "juillet": 7,
    "août": 8,
    "septembre": 9,
    "octobre": 10,
    "novembre": 11,
    "décembre": 12
}


def get_corresponding_month(month_name):
    """
    This function returns the numerical month corresponding to a month name in English.
    For example, "august" will return 8.

    :param month_name: The name of the month (case-insensitive).
    :return: The numerical value of the month.
    """
    return MONTH_MAP.get(month_name.lower())


def send_push_notification(title, message):
    """
    This function sends a push notification using the Pushbullet API.

    :param title: The title of the notification.
    :param message: The message of the notification.
    """
    try:
        pb = Pushbullet("o.oWmXGEvKma6mRIqdxDzwpwO9bNlVoyEj")
        pb.push_note(title, message)
        print("Notification sent successfully.")
    except Exception as e:
        print(f"Error sending the notification: {str(e)}")
