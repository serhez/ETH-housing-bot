import os
import time
import platform
import urllib.request
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


CHROME_DRIVER = ""
if platform.system() == "Windows":
    CHROME_DRIVER = os.getcwd() + "\\drivers\\chromedriver-win.exe"
elif platform.system() == "Darwin":
    CHROME_DRIVER = os.getcwd() + "/drivers/chromedriver-mac"
elif platform.system() == "Linux":
    CHROME_DRIVER = os.getcwd() + "/drivers/chromedriver-linux"

AUDIO_TO_TEXT_DELAY = 10
AUDIOS_PATH = os.getcwd() + "audios/"
AUDIO_FILE = "captcha.mp3"


# def audio_to_text(audio_file):
#     recognizer = sr.Recognizer()
#     with sr.AudioFile(AUDIOS_PATH + audio_file) as source:
#         # Listen for the data (load audio to memory)
#         audio_data = recognizer.record(source)
#         # Recognize (convert from speech to text)
#         text = recognizer.recognize_google(audio_data)
#         return text


# def download_captcha_audio(driver, file_name):
#     driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])
#     WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID ,"recaptcha-anchor"))).click()
#     time.sleep(1.2)
#     driver.switch_to.default_content()
#     WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[title='recaptcha challenge']")))
#     WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#recaptcha-audio-button"))).click()
#     time.sleep(1.4)
#     WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".rc-audiochallenge-play-button button")))

#     # Get audio src
#     for _ in range(10):
#         try:
#             src = driver.find_element_by_id("audio-source").get_attribute("src")
#             break
#         except NoSuchElementException:
#             print('Captcha audio source - Retry in 0.5 second')
#             time.sleep(0.5)
#     else:
#         raise NoSuchElementException

#     urllib.request.urlretrieve(src, AUDIOS_PATH + file_name)

#     return


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

# for _ in range(10):
#     try:
#         driver.find_elements_by_class_name('g-recaptcha')[0].find_element_by_tag_name('iframe').click()
#         break
#     except NoSuchElementException:
#         print('Captcha - Retry in 0.5 second')
#         time.sleep(0.5)
# else:
#     raise NoSuchElementException

# download_captcha_audio(driver, AUDIO_FILE)
# text = audio_to_text(AUDIO_FILE)
# print(text)

# driver.execute_script('''window.open("http://www.livingscience.ch/kontakt-studentenzimmer-zuerich/?L=0","_blank");''')

# test(driver, driver.window_handles[0], "Sergio Hernandez")
# test(driver, driver.window_handles[1], "Test name")

time.sleep(100)
driver.close()
