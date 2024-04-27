from components.job_applier import apply_to_job
from dotenv import load_dotenv
import os

load_dotenv()

def process_jobs(driver, db_connection):
    predefined_keywords = os.getenv("JOB_TITLE", "").lower().split(",")
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT job_id, job_title, job_link FROM jobs")
        jobs_data = cursor.fetchall()
        for job_data in jobs_data:
            job_id = job_data[0]
            job_title = job_data[1].lower()
            job_link = job_data[2]
            job_matched = False
            for keyword in predefined_keywords:
                if keyword in job_title:
                    apply_to_job(driver, db_connection, job_link)
                    job_matched = True
                    break
            if not job_matched:
                cursor.execute("UPDATE jobs SET status = %s WHERE job_id = %s", ("discarded", job_id))
                db_connection.commit()
                print("job discarded" + job_data[1])
    except Exception as e:
        print("Error processing jobs:", e)
    finally:
        cursor.close()

    # apply_to_job(driver, db_connection, "https://www.naukri.com/job-listings-software-engineer-developer-programmer-2024-graduate-can-also-appl-creative-hands-hr-noida-nagpur-pune-gurgaon-gurugram-delhi-ncr-mumbai-all-areas-0-to-2-years-090224005442")