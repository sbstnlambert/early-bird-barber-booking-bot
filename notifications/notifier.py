# notifications/notifier.py
from pushbullet import Pushbullet
from utils.helpers import get_corresponding_month


class Notifier:
    def __init__(self, api_key):
        """
        Initialise l'objet Notifier avec la clé d'API Pushbullet.
        """
        self.pb = Pushbullet(api_key)
        self.notified_dates = set()  # Un ensemble pour stocker les dates déjà notifiées

    def check_availability(self, appointment_date, calendar_date, calendar_day_elements):
        calendar_month, calendar_year = calendar_date.split(" ")
        in_sequence = False

        for calendar_day_element in calendar_day_elements:
            day_text = calendar_day_element.text.strip()

            if day_text.isnumeric():
                day_number = int(day_text)

                if day_number == 1:
                    # La séquence commence
                    in_sequence = True

                if in_sequence:
                    day_style = calendar_day_element.get_attribute("style")
                    calendar_month_num = get_corresponding_month(calendar_month)
                    calendar_year_num = int(calendar_year)

                    if "text-decoration: line-through" not in day_style and (
                            (calendar_year_num < appointment_date.year) or
                            (
                                    calendar_year_num == appointment_date.year and calendar_month_num < appointment_date.month) or
                            (
                                    calendar_year_num == appointment_date.year and calendar_month_num == appointment_date.month and day_number < appointment_date.day)
                    ):
                        # Vérifiez si la date a déjà été notifiée
                        if (calendar_year_num, calendar_month_num, day_number) not in self.notified_dates:
                            self.send_notification("Nouveau désistement !",
                                                   f"La date {day_number} {calendar_month} {calendar_year} est disponible pour un rendez-vous avec Gianni Basciu.")
                            # Ajoutez la date notifiée à l'ensemble
                            self.notified_dates.add((calendar_year_num, calendar_month_num, day_number))

                    # Vérifiez si le prochain jour est également 1, si oui, c'est le début du mois suivant et nous devons l'exclure
                    if calendar_day_elements.index(calendar_day_element) < len(calendar_day_elements) - 1:
                        next_day_element = calendar_day_elements[calendar_day_elements.index(calendar_day_element) + 1]
                        next_day_text = next_day_element.text.strip()
                        if next_day_text.isnumeric() and int(next_day_text) == 1:
                            in_sequence = False
                            break  # Sort de la boucle lorsque le mois suivant est atteint

    def send_notification(self, title, message):
        """
        Envoie une notification push avec le titre et le message spécifiés.
        """
        try:
            self.pb.push_note(title, message)
            print("Notification envoyée avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'envoi de la notification : {str(e)}")
