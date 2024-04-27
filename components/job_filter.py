from components.job_applier import apply_to_job
from dotenv import load_dotenv
import time
import random
import os

load_dotenv()

def get_applications_today_count(db_connection):
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM jobs WHERE DATE(timestamp) = CURDATE() AND status = 'applied';")
        applications_count = cursor.fetchone()[0]
        return applications_count
    except Exception as e:
        print("Error getting applications count") #:, e)
        return 0
    finally:
        cursor.close()
        
def process_jobs_if_under_limit(driver, db_connection):
    max_applications_per_day = 50
    applications_today_count = get_applications_today_count(db_connection)
    print("Applied today : "+ str(applications_today_count))
    if applications_today_count < max_applications_per_day:
        process_jobs(driver, db_connection)
    else:
        print("Already applied to the maximum number of jobs for today.")

def process_jobs(driver, db_connection):
    positive_job_title_keywords = os.getenv("POSITIVE_JOB_TITLE_KEYWORDS", "").lower().split(",")
    negative_job_title_keywords = os.getenv("NEGATIVE_JOB_TITLE_KEYWORDS", "").lower().split(",")
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT job_id, job_title, job_link FROM jobs WHERE status = 'not applied';")
        jobs_data = cursor.fetchall()
        for job_data in jobs_data:
            job_id = job_data[0]
            job_title = job_data[1].lower()
            job_link = job_data[2]
            job_positive_matched = False
            job_negative_matched = False
            for keyword in positive_job_title_keywords:
                if keyword in job_title:
                    job_positive_matched = True
                    break
            for keyword in negative_job_title_keywords:
                if keyword in job_title:
                    job_negative_matched = True
                    break
            if job_positive_matched and not job_negative_matched:
                apply_to_job(driver, db_connection, job_link)
            else:
                cursor.execute("UPDATE jobs SET status = %s WHERE job_id = %s", ("discarded", job_id))
                db_connection.commit()
                print("Job discarded : " + job_data[1])
    except Exception as e:
        print("Error processing jobs:", e)
    finally:
        cursor.close()
        sleep_time = random.randint(120, 360)
        time.sleep(sleep_time)

    # apply_to_job(driver, db_connection, "https://www.naukri.com/job-listings-software-engineer-developer-programmer-2024-graduate-can-also-appl-creative-hands-hr-noida-nagpur-pune-gurgaon-gurugram-delhi-ncr-mumbai-all-areas-0-to-2-years-090224005442")