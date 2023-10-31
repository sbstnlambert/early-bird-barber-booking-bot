import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import locale
from config.config import Config
from notifications.notifier import Notifier
import logging

# Set the locale explicitly to avoid errors
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'C.UTF-8')


def setup_chrome_driver(config):
    # Create a service object for ChromeDriver
    service = Service(config.CHROME_DRIVER_PATH)

    # Set Chrome options
    chrome_options = Options()

    # Launch the Chrome browser
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def toggle_barber_option(driver, wait, has_barber_option):
    # Toggle the barber option flag
    has_barber_option = not has_barber_option

    # Select the general category "Vip avec Gianni Basciu (+12€)"
    general_category = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='am-catalog']/div[1]/div[2]/div[1]/div/div[1]")))
    general_category.click()

    # Select the specific category "Coupe Homme Vip"
    specific_category = wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='am-category']/div[1]/div[2]/div[2]/div")))
    actions = webdriver.ActionChains(driver)
    actions.move_to_element(specific_category).perform()
    specific_category.click()

    if has_barber_option:
        add_option_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "am-add-element")))
        add_option_button.click()

        dropdown_menu = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                               "#am-step-booking-catalog0 > div.am-form-full-wrapper.am-form-catalogForm-selectServiceForm > div > form > div:nth-child(2) > span > div > div > div.el-col.el-col-14 > div > div")))
        dropdown_menu.click()

        select_barber_extra = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "body > div.el-select-dropdown.el-popper.am-dropdown-catalogForm-selectServiceForm > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul > li")))
        select_barber_extra.click()

    return has_barber_option


def check_appointment_availability(driver, notifier, wait):
    # TODO: Define your appointment date
    # i.e. below is the date 2024, February 9 at 10:00am
    appointment_date = datetime(2024, 2, 9, 10, 0)

    # Wait for the month element to be visible
    time.sleep(5)
    calendar_date_elements = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='am-calendar-picker']/div[1]/div[2]/div/div/div")))
    calendar_date = calendar_date_elements.text

    # Find all elements corresponding to the days of the month
    calendar_day_elements = driver.find_elements(By.CSS_SELECTOR,
                                                 "#am-calendar-picker > div > div.c-day-content-wrapper > div")

    # Check appointment availability
    notifier.check_availability(appointment_date, calendar_date, calendar_day_elements)


def main():
    # Initialize configuration
    config = Config()

    # TODO: Initialize Notifier with your Pushbullet API key between the quote marks.
    # i.e. notifier = Notifier("o.qYmXVTvKmb1mMVqdxDzwpw54bNlVoyQp")
    notifier = Notifier("")

    # Create a service object for ChromeDriver
    driver = setup_chrome_driver(config)

    # Initialize barber option bool
    has_barber_option = True

    try:
        # Open the appointment page
        driver.get(Config.URL)

        # Wait for the page to load
        wait = WebDriverWait(driver, 10)

        while True:
            has_barber_option = toggle_barber_option(driver, wait, has_barber_option)

            # Click the "Continuer" button to access the calendar
            continue_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "el-button--primary")))
            continue_button.click()

            check_appointment_availability(driver, notifier, wait)

            # Wait for 10 minutes before refreshing the page
            time.sleep(600)  # 10 minutes = 600 seconds

            # Refresh page
            driver.refresh()

    except Exception as e:
        # Initialize logging for better error handling
        logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(f"An error occurred: {str(e)}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
