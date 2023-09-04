# utils/helpers.py
from pushbullet import Pushbullet

# Crée un dictionnaire de correspondance entre les noms de mois et les mois numériques
month_map = {
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
    Cette fonction renvoie le mois numérique correspondant à un nom de mois en français.
    Par exemple, "août" renverra 8.
    """
    return month_map.get(month_name.lower())

def send_push_notification(title, message):
    """
    Cette fonction envoie une notification push en utilisant l'API Pushbullet.
    Elle prend un titre et un message en entrée.
    """
    try:
        pb = Pushbullet("o.oWmXGEvKma6mRIqdxDzwpwO9bNlVoyEj")
        pb.push_note(title, message)
        print("Notification envoyée avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de la notification : {str(e)}")