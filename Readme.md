This project is to automate repetative task in applying job



query to create required SQL database - 
CREATE TABLE jobs (
    job_id VARCHAR(255) NOT NULL PRIMARY KEY,
    status VARCHAR(255),
    job_title VARCHAR(255),
    company VARCHAR(255),
    experience VARCHAR(255),
    salary VARCHAR(255),
    location VARCHAR(255),
    description TEXT,
    job_link VARCHAR(512),
    timestamp TIMESTAMP
);



.env file needs to be created in components in following format:

# job search links
# search your job on naukri.com with required filters and devide the link like below with '?' in link as split point or just write code for it (am lazy)
LINK_PART_1 = "https://www.naukri.com/java-jobs-in-mumbai"
LINK_PART_2 = "?experience=0"

# naukri.com login details
EMAIL_ID = *naukri.com login email id*
PASSWORD = *naukri.com password*

# MySQL database details
DB_HOST = *mysql host (mostly localhost if using local data)*
DB_USER = *mysql user (mostly root)*
DB_PASSWORD = *mysql password*
DB_NAME = *database name*


run new_scraper.py first it will create database of job links
then run naukri.com-job-applier.py this will loop over each record and apply each job

every time naukri.com asks extra questions while applying a job on platform it will play notification.mp3 in assets folder
you need to manually enter data and click save/next, program will wait for you to do so

one a job is applied status of that job in database will change to "applied"

some job posting require visiting company website in order to apply 
these will be marked as "apply on company site" as status in database
you need to manually visit these sites and mark them as "applied"