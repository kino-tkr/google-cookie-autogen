from DrissionPage import ChromiumPage, ChromiumOptions
from pyvirtualdisplay import Display
import json
import time
import traceback
import os
import requests

def main():
    display = Display(visible=0, size=(1920, 1080))
    display.start()

    options = ChromiumOptions()
    options.set_argument('--no-sandbox')
    options.set_argument('--disable-dev-shm-usage')
    try:
        print("proxy", requests.get("https://api.ipify.org", proxies={"http": "http://localhost:8888", "https": "http://localhost:8888"}, timeout=3).text)
        options.set_argument('--proxy-server="http://localhost:8888"')
    except:
        print("proxyless", requests.get("https://api.ipify.org").text)
    #options.set_argument('--disable-blink-features=AutomationControlled')
    options.headless(False)

    page = ChromiumPage(options)
    page.get('https://www.google.com/search?q=a')
    time.sleep(5)

    captcha = False
    try:
        page.ele("#captcha-form", timeout=1)
        captcha = True
    except:
        pass

    if captcha:
        raise Exception("captcha detected")
    else:
        cookies = page.cookies()
        with open('cookies.json', 'w') as f:
            json.dump(cookies, f, indent=2)
        print("Cookies saved to cookies.json")

    page.get_screenshot(path='screenshot.png', full_page=True)
    page.quit()
    display.stop()

if __name__ == "__main__":
    main()
