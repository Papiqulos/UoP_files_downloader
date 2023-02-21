from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

path = 'D:\ACode\Python\Web Scraping\chromedriver.exe'


def test_eight_components():
    driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()))

    driver.get("https://www.selenium.dev/selenium/web/web-form.html")

    title = driver.title
    assert title == "Web form"

    driver.implicitly_wait(0.5)

    text_box = driver.find_element(by=By.NAME, value="my-text")
    submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

    time.sleep(2)
    text_box.send_keys("Selenium")
    time.sleep(2)

    submit_button.click()
    time.sleep(2)

    message = driver.find_element(by=By.ID, value="message")
    value = message.text
    assert value == "Received!"
    time.sleep(2)
    # driver.quit()


if __name__ == '__main__':
    test_eight_components()