from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from dotenv import load_dotenv
import mysql.connector
import time
import os

# Initialize WebDriver
options = Options()
options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
driver = webdriver.Firefox(options=options)

load_dotenv()

def login_to_naukri():
    try:
        driver.get('https://www.naukri.com/nlogin/login')
        time.sleep(5)
        username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "usernameField")))
        username_input.send_keys(os.getenv("EMAIL_ID"))
        password_input = driver.find_element(By.ID, "passwordField")
        password_input.send_keys(os.getenv("PASSWORD"))
        time.sleep(2)
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        login_button.click()
        print("Logged in successfully!")
    except TimeoutException:
        print("Login page not loaded or elements not found.")
        driver.quit()

def apply_to_job(job_link):
    try:
        driver.execute_script(f"window.open('{job_link}', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        # Dismiss any overlays or modals that might obscure the "Apply" button
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "modal-overlay")))
        time.sleep(3)
        apply_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "apply-button")))
        apply_button.click()
        time.sleep(5)
        update_status("applied", job_link)
        print("Applied to job at:", job_link)
    except TimeoutException:
        print("Apply button not found for job at:", job_link)
        print("Status: not applied")
    except NoSuchElementException:
        print("Apply button not found for job at:", job_link)
        print("Status: not applied")
    finally:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])


def update_status(status, job_link):
    try:
        cursor = db_connection.cursor()
        sql = "UPDATE jobs SET status = %s WHERE job_link = %s"
        val = (status, job_link)
        cursor.execute(sql, val)
        db_connection.commit()
        print("Status updated for job at:", job_link)
    except Exception as e:
        print("Error updating status:", e)
    finally:
        cursor.close()

def process_jobs():
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT job_link FROM jobs WHERE status = 'not applied'")
        job_links = cursor.fetchall()
        for job_link in job_links:
            apply_to_job(job_link[0])
    except Exception as e:
        print("Error processing jobs:", e)
    finally:
        cursor.close()

# Establish connection to MySQL database
try:
    db_connection = mysql.connector.connect(
        host= os.getenv("DB_HOST"),
        user= os.getenv("DB_USER"),
        password= os.getenv("DB_PASSWORD"),
        database= os.getenv("DB_NAME")
    )
    print("Connected to database successfully!")
    # Call the login function
    login_to_naukri()
    # Process jobs in the database
    process_jobs()
except mysql.connector.Error as error:
    print("Error connecting to database:", error)
finally:
    # Close database connection
    if 'db_connection' in locals() or 'db_connection' in globals():
        db_connection.close()
    # Quit WebDriver
    driver.quit()



# chatbot_DrawerContentWrapper
"""
<span class="apply-message">You have successfully applied to&nbsp;<strong>'Java Developer'</strong></span>
"""
"""
<span id="already-applied" class="styles_already-applied__4KDhw already-applied">Applied</span>
"""
