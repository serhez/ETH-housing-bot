import os
import re
import time
from datetime import datetime
import platform
import requests
import urllib.request
import webbrowser
import http.client, urllib
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


LS = 0
SV = 1
SV_FREI_COUNT = 1
CHECK_FREQUENCY = 1
ROOM_FOUND_WAIT = 60 * 10
BUILDING_STRINGS = ["LIVING SCIENCE", "STUDENT VILLAGE"]
URLS = ["http://reservation.livingscience.ch/en/living", "https://studentvillage.ch/en/accommodation/"]

CHROME_DRIVER = ""
if platform.system() == "Windows":
    CHROME_DRIVER = os.getcwd() + "\\drivers\\chromedriver-win.exe"
elif platform.system() == "Darwin":
    CHROME_DRIVER = os.getcwd() + "/drivers/chromedriver-mac"
elif platform.system() == "Linux":
    CHROME_DRIVER = os.getcwd() + "/drivers/chromedriver-linux"

PUSHOVER_APP_TOKEN = "axpsbeqx8zqtqf1t2n3fxgrftyhzr5"
PUSHOVER_USER_KEY = "uez8re7h4fz7t9t3fze12ag5gorpyy"


def is_ls_available(out_content):
    # Method 1
    content = requests.get(url=URLS[LS], params=None).content.decode("utf-8")
    if not re.search("nodata", content) or not re.search("No record available", content) or re.search("row status", content):
        out_content.append(content)
        return True

    return False


def is_sv_available(out_content):
    # Method 1
    content = requests.get(url=URLS[SV], params=None).content.decode("utf-8")
    if len(re.findall("frei", content)) > SV_FREI_COUNT:
        out_content.append(content)
        return True

    # Method 2
    match = re.search("wohnen_table(.*)ActiveRoomListRow", content, re.DOTALL)
    if match == None:
        print("Error: SV method 2's regex is not matching")
    else:
        content = match.group(0)
        if re.match("frei", content) or re.match("Available", content):
            out_content.append(content)
            return True

    return False


def open_ls_url():
    try: 
        webbrowser.open_new(URLS[LS])
    except: 
        print("Could not access Living Science website")
        return


def open_sv_url():
    try: 
        webbrowser.open_new(URLS[SV])
    except: 
        print("Could not access Student Village website")
        return


def notify(building):
    # On console
    print("\nFound an available room at " + BUILDING_STRINGS[building] + " [" + datetime.now().strftime("%H:%M:%S") + "]")
    
    # On Windows
#     toaster.show_toast(BUILDING_STRINGS[building],
#                        "A room is available",
#                        duration=None,
#                        threaded=True,
#                        callback_on_click= building == open_ls_url if LS else open_sv_url)
# 
    # On mobile
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
            "token": PUSHOVER_APP_TOKEN,
            "user": PUSHOVER_USER_KEY,
            "title": BUILDING_STRINGS[building],
            "message": "Room available at " + BUILDING_STRINGS[building],
            "url": URLS[building],
            "url_title": "GO",
            "priority": "2",
            "retry": "30",
            "expire": "10800"
        }), { "Content-type": "application/x-www-form-urlencoded" })
    if conn.getresponse().getcode() != 200:
        print("\nERROR: Connection to mobile push notifications is broken\n")
        return
    
    return


def ls_complete_form(driver, submit):
    # SECTION: Switch to correct tab

    # driver.switch_to.window(tab_handle)

    # SECTION: Click on email button
    for _ in range(2):
        try:
            driver.find_element_by_xpath("/html/body/div/div[4]/div[2]/div[2]/div[1]/div/div[2]/div/div/div/div/div[3]/div[2]/span[11]/a[2]").click()
            break
        except NoSuchElementException:
                print('Email button (1) - Retry in 0.25 second')
                time.sleep(0.25)
    else:
        for _ in range(1):
            try:
                driver.find_element_by_xpath('//*[@id="cimmotool_immotool_immotool_search"]/div[3]/div[2]/span[11]/a[2]').click()
                break
            except NoSuchElementException:
                    print('Email button (1) - Retry in 0.25 second')
                    time.sleep(0.25)
        else:
            for _ in range(1):
                try:
                    driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div[2]/div[1]/div/div[2]/div/div/div/div/div[3]/div[2]/span[11]/a[2]").click()
                    break
                except NoSuchElementException:
                    print('Email button (2) - Retry in 0.25 second')
                    time.sleep(0.25)
            else:
                for _ in range(10):
                    try:
                        driver.find_element_by_css_selector("#cimmotool_immotool_immotool_search > div.list.scroll > div.row.status1 > span.icons > a.ajaxloader").click()
                        break
                    except NoSuchElementException:
                        print('Email button (3) - Retry in 0.5 second')
                        time.sleep(0.5)
                else:
                    raise NoSuchElementException

    # SECTION: Complete form

    # Title
    for _ in range(10):
        try:
            Select(driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[2]/div[1]/div/select")).select_by_value("Herr")
            break
        except NoSuchElementException:
            print('Title - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise 

    # Surname
    for _ in range(10):
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[2]/div[2]/input").send_keys("Hernandez Gutierrez")
            break
        except NoSuchElementException:
            print('Surname - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # First name
    for _ in range(10):
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[2]/div[3]/input").send_keys("Sergio Christian")
            break
        except NoSuchElementException:
            print('First name - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # Street
    for _ in range(10):
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[2]/div[4]/div[1]/input").send_keys("Calle Los Helechos")
            break
        except NoSuchElementException:
            print('Street - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # Street number
    for _ in range(10):
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[2]/div[4]/div[3]/input").send_keys("13")
            break
        except NoSuchElementException:
            print('Street number - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # ZIP
    for _ in range(10):
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[2]/div[5]/div[1]/input").send_keys("38292")
            break
        except NoSuchElementException:
            print('ZIP - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # Place
    for _ in range(10):
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[2]/div[5]/div[3]/input").send_keys("Santa Cruz de Tenerife")
            break
        except NoSuchElementException:
            print('Place - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # Country
    for _ in range(10):
        try:
            Select(driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[2]/div[6]/div/select")).select_by_value("ES Spanien")
            break
        except NoSuchElementException:
            print('Country - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # Email
    for _ in range(10):
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[2]/div[7]/input").send_keys("contact.sergiohernandez@gmail.com")
            break
        except NoSuchElementException:
            print('Email - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # Telephone
    for _ in range(10):
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[2]/div[8]/input").send_keys("0034650802397")
            break
        except NoSuchElementException:
            print('Telephone - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # Date of birth
    for _ in range(10):
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[2]/div[9]/input").send_keys("02.06.1997")
            break
        except NoSuchElementException:
            print('Date of birth - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # Nationality
    for _ in range(10):
        try:
            Select(driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[2]/div[10]/div/select")).select_by_value("ES Spanien")
            break
        except NoSuchElementException:
            print('Nationality - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # Language
    for _ in range(10):
        try:
            Select(driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[2]/div[11]/div/select")).select_by_value("ES Spanisch")
            break
        except NoSuchElementException:
            print('Language - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # Income
    for _ in range(10):
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[2]/div[12]/input").send_keys("0")
            break
        except NoSuchElementException:
            print('Income - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # Civil status
    for _ in range(10):
        try:
            Select(driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[2]/div[13]/div/select")).select_by_value("ledig")
            break
        except NoSuchElementException:
            print('Civil status - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # Correspondece
    for _ in range(10):
        try:
            Select(driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[2]/div[14]/div/select")).select_by_value("Englisch")
            break
        except NoSuchElementException:
            print('Correspondence - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # Degree
    for _ in range(10):
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[5]/div[1]/input").send_keys("Masters in Computer Science")
            break
        except NoSuchElementException:
            print('Degree - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # Faculty
    for _ in range(10):
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[5]/div[3]/input").send_keys("Department of Computer Science")
            break
        except NoSuchElementException:
            print('Faculty - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # Start of studies
    for _ in range(10):
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[5]/div[4]/input").send_keys("21.09.2021")
            break
        except NoSuchElementException:
            print('Start of studies - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # End of study
    for _ in range(10):
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[5]/div[5]/input").send_keys("20.09.2023")
            break
        except NoSuchElementException:
            print('End of study - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # Rental agreement
    for _ in range(10):
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[4]/div[1]/div/input").click()
            break
        except NoSuchElementException:
            print('Rental agreement - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # House rules
    for _ in range(10):
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[4]/div[2]/div/input").click()
            break
        except NoSuchElementException:
            print('House rules - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # Confirmation
    for _ in range(10):
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[4]/div[3]/div/input").click()
            break
        except NoSuchElementException:
            print('Confirmation - Retry in 0.5 second')
            time.sleep(0.5)
    else:
        raise NoSuchElementException

    # SECTION: Submit

    if submit:
        # Wait to not trigger captcha
        time.sleep(1.5)

        # Captcha
        for _ in range(10):
            try:
                driver.find_elements_by_class_name("g-recaptcha")[0].find_element_by_tag_name('iframe').click()
                break
            except NoSuchElementException:
                print('Captcha - Retry in 0.5 second')
                time.sleep(0.5)
        else:
            raise NoSuchElementException

        # Wait for captcha
        time.sleep(1)

        # Submit button
        for _ in range(10):
            try:
                driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[5]/div[11]/button").click()
                break
            except NoSuchElementException:
                print('Submit button - Retry in 0.5 second')
                time.sleep(0.5)
        else:
            raise NoSuchElementException

    return


def ls_apply(driver):
    driver.get("http://reservation.livingscience.ch/wohnen")
    # driver.execute_script('''window.open("http://reservation.livingscience.ch/wohnen","_blank");''')

    try:
        ls_complete_form(driver, False)
        # ls_complete_form(driver, driver.window_handles[1], True)
    except NoSuchElementException:
        driver.close()
        return False

    time.sleep(ROOM_FOUND_WAIT)
    driver.close()

    return True


def get_ls_ids(content):
    # ids = []
    # matches = re.findall("whgnr(.*)<", content)
    # for match in matches:
    #     ids.append(match[8:-1])
    # return ids

    match = re.search("whgnr(.*)<", content)
    if match == None:
        print("Error: LS id extraction regex is not matching")
        return ""

    return match.group(0)[8:-1]


def get_ls_date(content):
    match = re.search("Start of rent:</span>(.*)<", content)
    if match == None:
        print("Error: LS date extraction regex is not matching")
        return ""

    return match.group(0)[8:-1]


def download_file(url, filename, extension):
    response = urllib.request.urlopen(url)    
    file = open(filename + "." + extension, 'wb')
    file.write(response.read())
    file.close()


def write_to_file(content, filename, extension):
    file = open(filename + "." + extension, "w")
    file.write(content)
    file.close()


def main():
    webbrowser.register('chrome',
        None,
        webbrowser.BackgroundBrowser("C://Program Files//Google//Chrome//Application//chrome.exe"))

    driver = webdriver.Chrome(CHROME_DRIVER)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument("--mute-audio")
    driver.maximize_window()

    found = []

    while(True):
        # Living Science (LS)
        out_content = []
        if is_ls_available(out_content):
            id = get_ls_ids(out_content[0])
            if id == "" or id not in found:
                notify(LS)
                ls_apply(driver)
                write_to_file(out_content[0], "data/living_science_src_" + datetime.now().strftime("%d-%m-%Y_%H-%M-%S"), "html")
                found.extend([id])
            else:
                print("Did not notify/apply to a room that already was found")

        # Student Village (SV)
        # out_content = []
        # if is_sv_available(out_content):
            # notify(SV)

        time.sleep(CHECK_FREQUENCY)


if __name__ == "__main__":
    main()
