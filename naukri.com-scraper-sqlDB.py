from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import csv
from datetime import datetime
import mysql.connector

def scrape_page():
    cursor = db_connection.cursor()

    for job_tuple in job_tuples:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            job_id = job_tuple.get_attribute('data-job-id')
            job_title_element = job_tuple.find_element(By.CLASS_NAME, 'title')
            job_title = job_title_element.text
            job_link = job_title_element.get_attribute('href')
            company = job_tuple.find_element(By.CLASS_NAME, 'comp-name').text
            experience = job_tuple.find_element(By.CLASS_NAME, 'expwdth').text
            salary = job_tuple.find_element(By.CLASS_NAME, 'sal').text
            location = job_tuple.find_element(By.CLASS_NAME, 'locWdth').text
            description = job_tuple.find_element(By.CLASS_NAME, 'job-desc').text
        except NoSuchElementException as e:
            print("Some job details not found for a job tuple:", e)
            continue
        
        sql = "INSERT INTO jobs (job_id, status, job_title, company, experience, salary, location, description, job_link, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (job_id, "not applied", job_title, company, experience, salary, location, description, job_link, timestamp)
        
        cursor.execute(sql, val)

    db_connection.commit()
    print("Recorded in the database")

    cursor.close()

# Establish connection to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="cyanZEUS",
    database="naukri_job_opening_data"
)

count = 1
while count < 10:
    geckodriver_path = "C:/Users/shubh/Projects/naukri.com-auto-apply/geckodriver.exe"
    options = Options()
    options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
    driver = webdriver.Firefox(service=Service(executable_path=geckodriver_path), options=options)
    if count == 1:
        driver.get('https://www.naukri.com/java-jobs?k=java&nignbevent_src=jobsearchDeskGNB&experience=0')
    else:
        driver.get('https://www.naukri.com/java-jobs'+ '-' + str(count) +'?k=java&nignbevent_src=jobsearchDeskGNB&experience=0')
    count += 1
    try:
        job_tuples = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'srp-jobtuple-wrapper')))
    except TimeoutException:
        print("Job tuples not found or page load timed out.")
        driver.quit()

    scrape_page()
    driver.quit()

# Close database connection
db_connection.close()
