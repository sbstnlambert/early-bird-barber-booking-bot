import logging
from pushbullet import Pushbullet
from utils.helpers import get_corresponding_month


class Notifier:
    """
    A class for checking appointment availability and sending notifications.
    """
    NOTIFICATION_TITLE = "Earlier Barber Appointment Available!"

    def __init__(self, api_key):
        """
        Initialize the Notifier instance.

        Args:
            api_key (str): The API key for Pushbullet.
        """
        self.pb = Pushbullet(api_key)
        self.notified_dates = set()
        self.logger = self.setup_logger()

    @staticmethod
    def setup_logger():
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def check_availability(self, appointment_date, calendar_date, calendar_day_elements,
                           notification_title=None):
        """
        Check appointment availability and send notifications.

        Args:
            appointment_date (datetime.date): The appointment date.
            calendar_date (str): The calendar date in a specific format.
            calendar_day_elements (list): List of calendar day elements.
            notification_title (str): The title for notifications.

        Returns:
            None
        """
        notification_title = notification_title or self.NOTIFICATION_TITLE
        calendar_month, calendar_year = calendar_date.split(" ")
        in_sequence = False

        for current_day_index, calendar_day_element in enumerate(calendar_day_elements):
            day_text = calendar_day_element.text.strip()

            if day_text.isnumeric():
                day_number = int(day_text)

                if day_number == 1:
                    in_sequence = True

                if in_sequence:
                    calendar_month_num = get_corresponding_month(calendar_month)
                    calendar_year_num = int(calendar_year)
                    is_available = self.is_date_available(calendar_day_element, appointment_date, calendar_month_num,
                                                          calendar_year_num)

                    if is_available:
                        message = f"Great news! An earlier slot at the barber just opened up on {day_number} {calendar_month} {calendar_year}. You can now get your hair done sooner than expected!"
                        self.notify_available_date(notification_title, message)
                        self.notified_dates.add((calendar_year_num, calendar_month_num, day_number))

                    if self.is_start_of_next_month(calendar_day_element, current_day_index, calendar_day_elements):
                        in_sequence = False
                        break

    @staticmethod
    def is_date_available(calendar_day_element, appointment_date, calendar_month_num, calendar_year_num):
        day_style = calendar_day_element.get_attribute("style")
        return (
                "text-decoration: line-through" not in day_style
                and (
                        calendar_year_num < appointment_date.year
                        or (
                                calendar_year_num == appointment_date.year
                                and calendar_month_num < appointment_date.month
                        )
                        or (
                                calendar_year_num == appointment_date.year
                                and calendar_month_num == appointment_date.month
                                and int(calendar_day_element.text.strip()) < appointment_date.day
                        )
                )
        )

    def notify_available_date(self, title, message):
        try:
            self.pb.push_note(title, message)
            self.logger.info("Notification sent successfully.")
        except Exception as e:
            self.logger.error(f"Error sending the notification: {str(e)}")

    @staticmethod
    def is_start_of_next_month(calendar_day_element, current_day_index, calendar_day_elements):
        next_day_index = current_day_index + 1
        if next_day_index < len(calendar_day_elements):
            next_day_element = calendar_day_elements[next_day_index]
            next_day_text = next_day_element.text.strip()
            return next_day_text.isnumeric() and int(next_day_text) == 1
        return False
