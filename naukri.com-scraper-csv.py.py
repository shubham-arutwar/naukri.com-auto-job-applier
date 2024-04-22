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

geckodriver_path = "C:/Users/shubh/Projects/naukri.com-auto-apply/geckodriver.exe"
options = Options()
options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
driver = webdriver.Firefox(service=Service(executable_path=geckodriver_path), options=options)
driver.get('https://www.naukri.com/java-jobs?k=java&nignbevent_src=jobsearchDeskGNB&experience=0')

try:
    job_tuples = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'srp-jobtuple-wrapper')))
except TimeoutException:
    print("Job tuples not found or page load timed out.")
    driver.quit()

# Create a CSV file to store the scraped data
csv_file = open('naukri_jobs.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Timestamp', 'Job Title', 'Company'])

# Iterate over each job tuple and extract relevant data
for job_tuple in job_tuples:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        job_title_element = job_tuple.find_element(By.CLASS_NAME, 'title')
        job_title = job_title_element.text
        job_link = job_title_element.get_attribute('href')  # Extracting the link
        company = job_tuple.find_element(By.CLASS_NAME, 'comp-name').text
        experience = job_tuple.find_element(By.CLASS_NAME, 'expwdth').text
        salary = job_tuple.find_element(By.CLASS_NAME, 'sal').text
        location = job_tuple.find_element(By.CLASS_NAME, 'locWdth').text
        description = job_tuple.find_element(By.CLASS_NAME, 'job-desc').text
    except NoSuchElementException as e:
        print("Some job details not found for a job tuple:", e)
        continue
    
    # Write the data to the CSV file
    csv_writer.writerow([timestamp, job_title, company, experience, salary, location, description, job_link])

csv_file.close()

