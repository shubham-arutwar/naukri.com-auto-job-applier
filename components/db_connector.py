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

load_dotenv()

def connection():
    db_connection = mysql.connector.connect(
        host= os.getenv("DB_HOST"),
        user= os.getenv("DB_USER"),
        password= os.getenv("DB_PASSWORD"),
        database= os.getenv("DB_NAME")
    )
    return db_connection

def update_status(db_connection, status, job_link):
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
        