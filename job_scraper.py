from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
from datetime import datetime
import os
import time
import mysql.connector
from components.db_connector import connection

load_dotenv()
options = Options()
options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"

def scrape_page(driver, db_connection):
    try:
        time.sleep(2)
        print("first try block")
        job_tuples = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'srp-jobtuple-wrapper')))
        print("job tuple created")
        cursor = db_connection.cursor()
        for job_tuple in job_tuples:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                job_id = job_tuple.get_attribute('data-job-id')
                # Check if the record already exists in the database
                cursor.execute("SELECT job_id FROM jobs WHERE job_id = %s", (job_id,))
                existing_record = cursor.fetchone()
                if existing_record:
                    print("Record already exists for job ID:", job_id)
                    continue  # Skip insertion
                else:
                    print("New record added for job ID:", job_id)
                job_title_element = job_tuple.find_element(By.CLASS_NAME, 'title')
                job_title = job_title_element.text
                job_link = job_title_element.get_attribute('href')
                company = job_tuple.find_element(By.CLASS_NAME, 'comp-name').text
                experience = job_tuple.find_element(By.CLASS_NAME, 'expwdth').text
                salary = job_tuple.find_element(By.CLASS_NAME, 'sal').text
                location = job_tuple.find_element(By.CLASS_NAME, 'locWdth').text
                description = job_tuple.find_element(By.CLASS_NAME, 'job-desc').text
            except NoSuchElementException as e:
                print("Some details may not be scraped")  #, e)
                continue
            sql = "INSERT INTO jobs (job_id, status, job_title, company, experience, salary, location, description, job_link, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (job_id, "not applied", job_title, company, experience, salary, location, description, job_link, timestamp)
            cursor.execute(sql, val)
        db_connection.commit()
        print("Recorded in the database")
        cursor.close()
        print("Cursor closed")   
        driver.quit()   
    except TimeoutException:
        print("Job tuples not found or page load timed out.")
        driver.quit()

try:
    db_connection = connection()
    print("Connected to database successfully!")
    count = 1
    while count < 20:
        driver = webdriver.Firefox(options=options)
        new_link = os.getenv("LINK_PART_1")+ '-' + str(count) +os.getenv("LINK_PART_2")
        print(new_link)
        driver.get(new_link)
        count += 1
        print("Page opened")
        scrape_page(driver, db_connection)
except mysql.connector.Error as error:
    print("Error connecting to database:", error)
finally:
    if 'db_connection' in locals() or 'db_connection' in globals():
        db_connection.close()
    driver.quit()
