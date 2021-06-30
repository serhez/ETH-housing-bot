import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


# TODO: Abrir una pagina que lo intente hacer automatico y otra que solo auto rellene

def test(driver, tab_handle, name):
    driver.switch_to.window(tab_handle)

    # Free text
    for i in range(10):
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/div[2]/form/fieldset/div[2]/input").send_keys(name)
            break
        except NoSuchElementException as e:
            print('Name - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise e

    # Dropdowns
    # Select(driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/div[2]/form/fieldset/div[1]/select")).select_by_index(1)
    for i in range(10):
        try:
            Select(driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/div[2]/form/fieldset/div[1]/select")).select_by_value("Herr")
            break
        except NoSuchElementException as e:
            print('Title - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise e

    # Checkboxes
    for i in range(10):
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/div[2]/form/fieldset/div[9]/fieldset/div/div/input").click()
            break
        except NoSuchElementException as e:
            print('License - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise e

    # Buttons
    # for i in range(10):
    #     try:
    #         driver.find_element_by_xpath("").click()
    #         break
    #     except NoSuchElementException as e:
    #         print('Retry in 0.5 second')
    #         time.sleep(0.5)
    # else:
    #     raise e

chrome_path = './chromedriver'
driver = webdriver.Chrome(chrome_path)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-popup-blocking")

driver.maximize_window()

driver.get("http://www.livingscience.ch/kontakt-studentenzimmer-zuerich/?L=0")
# os = platform.system()
# key = Keys.CONTROL
# if os == "Darwin":
#     key = Keys.COMMAND
# for i in range(10):
#     try:
#         ActionChains(driver).key_down(key).send_keys('t').key_up(key).perform()
#         break
#     except NoSuchElementException as e:
#         print('Creating tab - Retry in 0.5 second')
#         time.sleep(0.5)
# else:
#     raise
# driver.get("http://www.livingscience.ch/kontakt-studentenzimmer-zuerich/?L=0")
driver.execute_script('''window.open("http://www.livingscience.ch/kontakt-studentenzimmer-zuerich/?L=0","_blank");''')

test(driver, driver.window_handles[0], "Sergio Hernandez")
test(driver, driver.window_handles[1], "Test name")

time.sleep(100)
driver.close()