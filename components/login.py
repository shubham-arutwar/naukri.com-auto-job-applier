from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import time
import os

load_dotenv()

def login_to_naukri(driver):
    try:
        driver.get('https://www.naukri.com/nlogin/login')
        time.sleep(1)
        username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "usernameField")))
        username_input.send_keys(os.getenv("EMAIL_ID"))
        password_input = driver.find_element(By.ID, "passwordField")
        password_input.send_keys(os.getenv("PASSWORD"))
        time.sleep(1)
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        login_button.click()
        print("Logged in successfully!")
    except TimeoutException:
        print("Login page not loaded or elements not found.")
        driver.quit()