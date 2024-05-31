from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_data(username, password):
    driver = webdriver.Chrome()
    tasks = []
    courses = []

    try:
        driver.get('https://ncueeclass.ncu.edu.tw/')
        time.sleep(2)

        username_field = driver.find_element(By.NAME, 'account')
        username_field.send_keys(username)
        time.sleep(2)
        password_field = driver.find_element(By.NAME, 'password')
        password_field.send_keys(password)
        time.sleep(2)
        password_field.send_keys(Keys.RETURN)
        time.sleep(2)

        try:
            keep_login_button = driver.find_element(By.CLASS_NAME, 'keepLoginBtn')
            keep_login_button.click()
            time.sleep(2)
        except NoSuchElementException:
            print("Keep login button not found, proceeding with login")
        time.sleep(2)

        courses_element = driver.find_element(By.XPATH, '//*[@id="xbox2-inline"]/div[2]')
        course_list = courses_element.find_element(By.XPATH, '//*[@id="xbox2-inline"]/div[2]/div/div[2]/div/ul')
        course_items = course_list.find_elements(By.TAG_NAME, 'li')

        for item in course_items:
            course_name = item.find_element(By.CLASS_NAME, 'fs-label').text.strip()
            courses.append(course_name)

        more_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="/dashboard/latestEvent"]//span[text()="更多"]'))
        )
        more_link.click()
        time.sleep(2)

        table = driver.find_element(By.ID, 'recentEventTable')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        for row in rows[1:]:
            columns = row.find_elements(By.TAG_NAME, 'td')
            title = columns[0].text.strip()
            source = columns[1].text.strip()
            deadline = columns[2].text.strip()
            tasks.append({"title": title, "source": source, "deadline": deadline})

    finally:
        driver.quit()
    
    return tasks, courses