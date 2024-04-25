from components.applyJobs import apply_to_job

def process_jobs(driver, db_connection):
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT job_link FROM jobs")
        job_links = cursor.fetchall()
        for job_link in job_links:
            apply_to_job(driver, db_connection, job_link[0])
    except Exception as e:
        print("Error processing jobs:", e)
    finally:
        cursor.close()
    #apply_to_job(driver, db_connection, "https://www.naukri.com/job-listings-python-developer-nexpro247-mumbai-pune-chennai-0-to-5-years-040424005950")