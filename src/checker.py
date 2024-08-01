from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import src.config as config
from src.notifier import send_email, send_sms
from chromedriver_py import binary_path

def login_and_navigate(driver):
    driver.get("https://ais.usvisa-info.com/en-ca/niv/users/sign_in")

    username = driver.find_element(By.ID, "user_email")
    password = driver.find_element(By.ID, "user_password")
    username.send_keys(config.USERNAME)
    password.send_keys(config.PASSWORD)

    privacy_checkbox = driver.find_element(By.ID, "policy_confirmed")
    if not privacy_checkbox.is_selected():
        privacy_checkbox.send_keys(Keys.SPACE)

    password.send_keys(Keys.RETURN)

    # Wait for the URL to change to the desired page after login
    WebDriverWait(driver, 10).until(EC.url_contains("groups"))

    continue_button = driver.find_elements(By.CLASS_NAME, "primary")
    continue_button[0].click()

    time.sleep(5)  # Wait for the continue process to complete

    # Wait for the URL to change to the desired page after continue button click
    WebDriverWait(driver, 10).until(EC.url_contains("schedule"))

def get_appointment_dates(driver):
    try:
        # Find all accordion items
        accordion_items = driver.find_elements(By.CLASS_NAME, "accordion-item")
        
        # Check if there are at least 5 items
        if len(accordion_items) >= 5:
            fifth_item = accordion_items[3]  # 5th item (index 3)
            
            # Find the anchor tag within the 5th item and click it
            anchor_tag = fifth_item.find_element(By.TAG_NAME, "a")
            anchor_tag.click()

            time.sleep(5)  # Wait for the navigation process to complete

            small_only_expanded = driver.find_elements(By.CLASS_NAME, "small-only-expanded")

            # Loop through elements to find the one with the desired text
            for element in small_only_expanded:
                if "Reschedule Appointment" in element.text:
                    element.click()
                    break  # Exit the loop after clicking the desired element

            # Wait for the URL to change to the desired page after reschedule appointment click
            WebDriverWait(driver, 10).until(EC.url_contains("appointment"))

            # Find the dropdown element
            select_element = driver.find_element(By.ID, "appointments_consulate_appointment_facility_id")
            select = Select(select_element)

            # Read the desired location from the config file
            desired_location = config.DESIRED_LOCATION  # Ensure this is defined in your config file, e.g., "Toronto"

            # Select the option with the desired location
            for option in select.options:
                if option.text == desired_location:
                    select.select_by_visible_text(desired_location)
                    break

            time.sleep(5)  # Wait for the navigation process to complete

            # Example: finding all available appointment dates (assuming they have a specific class)
            appointment_dates_elements = driver.find_elements(By.CLASS_NAME, "appointment_date")
            appointment_dates = [date_element.text for date_element in appointment_dates_elements]

            print("Available appointment dates:", appointment_dates)

            return appointment_dates
        else:
            print("Less than 5 accordion items found.")
            return []
    except Exception as e:
        print("An error occurred:", e)
        return []

def check_dates(dates):
    start_date = datetime.strptime(config.START_DATE, '%Y-%m-%d')
    end_date = datetime.strptime(config.END_DATE, '%Y-%m-%d')
    for date in dates:
        appointment_date = datetime.strptime(date, '%Y-%m-%d')
        if start_date <= appointment_date <= end_date:
            return True
    return False

def main():
    # Define path to ChromeDriver
    chrome_driver_path = binary_path

    # Set up Chrome options (optional)
    chrome_options = Options()

    # Set up the ChromeDriver service
    service = Service(executable_path=chrome_driver_path)

    # Initialize WebDriver with service and options
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Perform login and initial navigation
    login_and_navigate(driver)

    # Repeat date checking 5 times
    for _ in range(5):
        dates = get_appointment_dates(driver)
        if check_dates(dates):
            send_email()
            send_sms()
        time.sleep(10)  # Wait for a short interval before checking again

    driver.quit()

