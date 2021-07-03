import os
import platform
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from selenium.common.exceptions import NoSuchElementException


CHROME_DRIVER = ""
if platform.system() == "Windows":
    CHROME_DRIVER = os.getcwd() + "\\chromedriver-win.exe"
elif platform.system() == "Darwin":
    CHROME_DRIVER = os.getcwd() + "/chromedriver-mac"
elif platform.system() == "Linux":
    CHROME_DRIVER = os.getcwd() + "/chromedriver-linux"


def test(driver, tab_handle, name):
    driver.switch_to.window(tab_handle)

    # Free text
    for _ in range(10):
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/div[2]/form/fieldset/div[2]/input").send_keys(name)
            break
        except NoSuchElementException:
            print('Name - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # Dropdowns
    # Select(driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/div[2]/form/fieldset/div[1]/select")).select_by_index(1)
    for _ in range(10):
        try:
            Select(driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/div[2]/form/fieldset/div[1]/select")).select_by_value("Herr")
            break
        except NoSuchElementException:
            print('Title - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # Checkboxes
    for _ in range(10):
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/div[2]/form/fieldset/div[9]/fieldset/div/div/input").click()
            break
        except NoSuchElementException:
            print('License - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # Buttons
    # for _ in range(10):
    #     try:
    #         driver.find_element_by_xpath("").click()
    #         break
    #     except NoSuchElementException as e:
    #         print('Retry in 0.5 second')
    #         time.sleep(0.5)
    # else:
    #     raise NoSuchElementException

driver = webdriver.Chrome(CHROME_DRIVER)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument("--mute-audio")

driver.maximize_window()

driver.get("https://www.google.com/recaptcha/api2/demo")

# Wait to not trigger captcha
time.sleep(2.1)

for i in range(10):
    try:
        driver.find_elements_by_class_name('g-recaptcha')[0].find_element_by_tag_name('iframe').click()
        break
    except NoSuchElementException as e:
        print('Captcha - Retry in 0.5 second')
        time.sleep(0.5)
else:
    raise NoSuchElementException


# driver.execute_script('''window.open("http://www.livingscience.ch/kontakt-studentenzimmer-zuerich/?L=0","_blank");''')

# test(driver, driver.window_handles[0], "Sergio Hernandez")
# test(driver, driver.window_handles[1], "Test name")

time.sleep(100)
driver.close()
