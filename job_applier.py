from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import mysql.connector
from components.login import login_to_naukri
from components.db_connector import connection
from components.job_filter import process_jobs

options = Options()
options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
driver = webdriver.Firefox(options=options)

try:
    db_connection = connection()
    print("Connected to database successfully!")
    login_to_naukri(driver)
    process_jobs(driver, db_connection)
except mysql.connector.Error as error:
    print("Error connecting to database:", error)
finally:
    if 'db_connection' in locals() or 'db_connection' in globals():
        db_connection.close()
        print("---END---")
    driver.quit()