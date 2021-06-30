import os
import re
import time
from datetime import datetime
import requests
import urllib.request
import webbrowser
import http.client, urllib
from win10toast_click import ToastNotifier
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


LS = 0
SV = 1
SV_FREI_COUNT = 1
CHECK_FREQUENCY = 1
BUILDING_STRINGS = ["LIVING SCIENCE", "STUDENT VILLAGE"]
URLS = ["http://reservation.livingscience.ch/en/living", "https://studentvillage.ch/en/accommodation/"]
CHROME_DRIVER = os.getcwd() + "/chromedriver"

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
    content = re.search("wohnen_table(.*)ActiveRoomListRow", content, re.DOTALL).group(0)
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


def notify(toaster, building):
    # On console
    print("\nFound an available room at " + BUILDING_STRINGS[building] + " [" + datetime.now().strftime("%H:%M:%S") + "]")
    
    # On Windows
    toaster.show_toast(BUILDING_STRINGS[building],
                       "A room is available",
                       duration=None,
                       threaded=True,
                       callback_on_click= building == open_ls_url if LS else open_sv_url)

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


def ls_complete_form(driver):
    # TODO: Click on email button

    # TODO: Complete form

    # TODO: Click on captcha button

    # TODO: Click on send button

    return


def ls_apply():
    driver = webdriver.Chrome(chrome_path)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-popup-blocking")

    driver.maximize_window()
    driver.get("http://reservation.livingscience.ch/wohnen")

    ls_complete_form(driver)

    return


def get_ls_ids(content):
    # ids = []
    # matches = re.findall("whgnr(.*)<", content)
    # for match in matches:
    #     ids.append(match[8:-1])
    # return ids

    return re.search("whgnr(.*)<", content).group(0)[8:-1]


def get_ls_date(content):
    try:
        return re.search("Start of rent:</span>(.*)<", content).group(0)[8:-1]
    except:
        print("Could not obtain the start of rent date")
        return ""


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
    toaster = ToastNotifier()
    webbrowser.register('chrome',
        None,
        webbrowser.BackgroundBrowser("C://Program Files//Google//Chrome//Application//chrome.exe"))

    found = []

    while(True):
        # Living Science (LS)
        out_content = []
        if is_ls_available(out_content):
            id = get_ls_ids(out_content[0])
            if id not in found:
                # TODO: If starting date is greater than August
                if (True):
                    ls_apply()
                notify(toaster, LS)
                write_to_file(out_content[0], "living_science_src_" + datetime.now().strftime("%d-%m-%Y_%H-%M-%S"), "html")
                found.extend([id])
            else:
                print("Did not notify/apply to a room that already was found")
                            
        # Student Village (SV)
        out_content = []
        if is_sv_available(out_content):
            if notify(toaster, SV, last_notif):
                last_notif = time.time()

        time.sleep(CHECK_FREQUENCY)


if __name__ == "__main__":
    main()