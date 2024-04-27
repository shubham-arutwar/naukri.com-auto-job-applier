# Naukri.com-auto-job-applier

## DISCLAIMER
There is a daily limit on the number of jobs you can apply for, typically capped at around 50 easy apply and 50 'on company site'.
`There was an error while processing your request, please try again later`
message will appear on websites when you hit the limit.

## Project Overview

This project automates the repetitive task of applying for jobs on Naukri.com. It scrapes job listings, stores them in a SQL database, and automatically applies to each job then updates its status in database.


## Database Schema
query to create table

```
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
    timestamp TIMESTAMP,
    platform VARCHAR(255)
);
```

## .env File Configuration

Create a .env file in the components directory with the following format:
- search your job on naukri.com with required filters and devide the link like below with '?' in link as split point `or just write code for it (am lazy)`
```
# job search links
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

# keywords for job title filtering
POSITIVE_JOB_TITLE_KEYWORDS= *write keywords for job title that you want to apply | constrains : without (), all lower, no spaces | eg-(java,python,analyst)*
NEGATIVE_JOB_TITLE_KEYWORDS= *write keywords for job title that you ABSOLUTELY DON'T want to apply | constrains : without (), all lower, no spaces | eg-(testing,devops)*
# logic is in ./components/job_filter.py
```

## pip packages required -
```pip install selenium python-dotenv mysql-connector-python pygame```


## Usage

- Run job_scraper.py to create a database of job links.
- Run job_applier.py to loop over each record and apply to each job.
- Every time naukri.com asks extra questions while applying a job on platform it will play notification.mp3 in assets folder.
- When prompted, manually enter any additional information required by Naukri.com during the application process.
- If some job postings require visiting the company website to apply, mark them as "applied" manually in the database. `job-id from naukri.com is primary key in database`

## Additional Notes

- If Naukri.com asks additional questions during the application process, notification.mp3 in the assets folder will play, indicating that manual input is required.
- Some job postings may require visiting the company website to apply. These will be marked as "apply on company site" in the database.

