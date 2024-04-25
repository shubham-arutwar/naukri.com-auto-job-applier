from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from components.dbConnection import update_status
from components.notificationSound import bruh

def apply_to_job(driver, db_connection, job_link):
    try:
        driver.execute_script(f"window.open('{job_link}', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "modal-overlay")))
        time.sleep(3)
        status = ""
        try:
            apply_button = driver.find_element(By.ID, "apply-button")
            apply_button.click()
            status = "applied"
            time.sleep(2)
            chatbot_present = driver.find_elements(By.CLASS_NAME, "chatbot_DrawerContentWrapper")
            while chatbot_present:
                bruh()
                time.sleep(1)
                print("while loop 5 sec sleep ends")
                chatbot_present = driver.find_elements(By.CLASS_NAME, "chatbot_DrawerContentWrapper")
            if not driver.find_elements(By.CLASS_NAME, "chatbot_DrawerContentWrapper"):
                success_message = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//span[@class='apply-message']")))
                print("30 sec timeout")
        except (NoSuchElementException, TimeoutException):
            try:
                already_applied_span = driver.find_element(By.ID, "already-applied")
                status = "applied"
            except NoSuchElementException:
                try:
                    company_site_button = driver.find_element(By.ID, "company-site-button")
                    status = "apply on company site"
                except NoSuchElementException:
                    print("status failed")
                    status = "failed"
        update_status(db_connection, status, job_link)
        print("Applied to job at:", job_link)
    except TimeoutException:
        print("Apply button not found for job at:", job_link)
        print("Status: not applied")
    except NoSuchElementException:
        print("Apply button not found for job at:", job_link)
        print("Status: not applied")
    finally:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])