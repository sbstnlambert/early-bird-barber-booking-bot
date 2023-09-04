import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import locale
from config.config import Config
from notifications.notifier import Notifier

# Définissez la locale explicitement pour éviter les erreurs
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'C.UTF-8')

def main():
    # Initialize configuration
    config = Config()

    # Initialize Notifier with Pushbullet API key
    notifier = Notifier("o.oWmXGEvKma6mRIqdxDzwpwO9bNlVoyEj")

    # Create a service object for ChromeDriver
    service = Service(config.CHROME_DRIVER_PATH)

    # Set Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")

    # Launch the Chrome browser
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Initialize barber option bool
    has_barber_option = False

    try:
        # Open the appointment page
        driver.get(config.URL)

        # Wait for the page to load
        wait = WebDriverWait(driver, 10)

        while True:

            # Toggle the barber option flag
            has_barber_option = not has_barber_option

            # Select the general category "Vip avec Gianni Basciu (+12€)"
            general_category = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='am-catalog']/div[1]/div[2]/div[1]/div/div[1]")))
            general_category.click()

            # Select the specific category "Coupe Homme Vip"
            specific_category = wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='am-category']/div[1]/div[2]/div[2]/div")))
            actions = ActionChains(driver)
            actions.move_to_element(specific_category).perform()
            specific_category.click()

            if has_barber_option:
                add_option_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "am-add-element")))
                add_option_button.click()

                dropdown_menu = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#am-step-booking-catalog0 > div.am-form-full-wrapper.am-form-catalogForm-selectServiceForm > div > form > div:nth-child(2) > span > div > div > div.el-col.el-col-14 > div > div")))
                dropdown_menu.click()

                select_barber_extra = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.el-select-dropdown.el-popper.am-dropdown-catalogForm-selectServiceForm > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul > li")))
                select_barber_extra.click()

            # Click the "Continuer" button to access the calendar
            continue_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "el-button--primary")))
            continue_button.click()

            # Define the appointment date
            appointment_date = datetime(2023, 12, 29, 10, 0)

            # Wait for the month element to be visible
            time.sleep(5)
            calendar_date_elements = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='am-calendar-picker']/div[1]/div[2]/div/div/div")))
            calendar_date = calendar_date_elements.text

            # Find all elements corresponding to the days of the month
            calendar_day_elements = driver.find_elements(By.CSS_SELECTOR, "#am-calendar-picker > div > div.c-day-content-wrapper > div")

            # Check appointment availability
            notifier.check_availability(appointment_date, calendar_date, calendar_day_elements)

            # Wait for 10 minutes before refreshing the page
            time.sleep(600)  # 10 minutes = 600 seconds

            # Refresh page
            driver.refresh()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
