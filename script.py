from DrissionPage import ChromiumPage, ChromiumOptions
from pyvirtualdisplay import Display
import json
import time
import sys
import random
import traceback
import os

tinyproxy_template = """Port 8888
Listen 127.0.0.1
Timeout 600
Allow 127.0.0.1
Upstream http {}
LogLevel Info"""

def random_proxy(proxy):
    try:
        os.mkdir("/etc/tinyproxy")
    except:
        pass
    proxy = proxy.replace(":1080", f":{random.randint(1080, 1380)}")
    open("/etc/tinyproxy/tinyproxy.conf", "w", encoding="utf_8").write(tinyproxy_template.format(proxy)
    os.system("tinyproxy")

def main():
    display = Display(visible=0, size=(1920, 1080))
    display.start()

    options = ChromiumOptions()
    options.set_argument('--no-sandbox')
    options.set_argument('--disable-dev-shm-usage')
    try:
        random_proxy(sys.argv[1])
        options.set_argument('--proxy-server="http://localhost:8888"')
    except:
        pass
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
