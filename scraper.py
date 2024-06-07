from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def get_data(username, password):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=options)

    try:
        # Navigate to the login page
        driver.get("https://portal.ncu.edu.tw/login")
        time.sleep(20)
        # Input username
        username_field = driver.find_element(By.NAME, 'username')
        username_field.send_keys(username)
        time.sleep(5)

        # Input password
        password_field = driver.find_element(By.NAME, 'password')
        password_field.send_keys(password)
        time.sleep(10)

        # Click login button
        in_button = driver.find_element(By.CLASS_NAME, 'btn-primary')
        in_button.click()
        time.sleep(3)

        # Click the element in recent apps
        element_to_click = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="recent-apps"]/li[1]/a[2]'))
        )
        element_to_click.click()
        time.sleep(5)

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])
        
        # Extract course information
        courses = []
        try:
            courses_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="xbox2-inline"]/div[2]'))
            )
            course_list = courses_element.find_element(By.XPATH, '//*[@id="xbox2-inline"]/div[2]/div/div[2]/div/ul')
            course_items = course_list.find_elements(By.TAG_NAME, 'li')
            
            for item in course_items:
                course_name = item.find_element(By.CLASS_NAME, 'fs-label').text.strip()
                courses.append(course_name)
        except TimeoutException:
            print("Courses element not found in the given time.")

        # Click "More" link
        more_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="/dashboard/latestEvent"]//span[text()="更多"]'))
        )
        more_link.click()
        time.sleep(3)

        # Extract recent events information
        tasks = []
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'recentEventTable'))
        )
        rows = table.find_elements(By.TAG_NAME, 'tr')
        for row in rows[1:]:
            columns = row.find_elements(By.TAG_NAME, 'td')
            title = columns[0].text.strip()
            source = columns[1].text.strip()
            deadline = columns[2].text.strip()
            tasks.append({"title": title, "source": source, "deadline": deadline})

        # Print extracted information (or process further)
        print("Courses:", courses)
        print("Tasks:", tasks)

    finally:
        # Quit the driver
        driver.quit()
    return tasks, courses