from DrissionPage import ChromiumPage, ChromiumOptions
from pyvirtualdisplay import Display
import json
import time

def main():
    # 仮想ディスプレイを起動
    display = Display(visible=0, size=(1920, 1080))
    display.start()

    options = ChromiumOptions()
    options.set_argument('--no-sandbox')
    options.set_argument('--disable-dev-shm-usage')
    #options.set_argument('--disable-blink-features=AutomationControlled')
    options.headless(False)

    page = ChromiumPage(options)
    page.get('https://www.google.com/search?q=a')
    time.sleep(3)

    cookies = page.cookies()
    with open('cookies.json', 'w') as f:
        json.dump(cookies, f, indent=2)
    page.screenshot('screenshot.png')

    print("Cookies saved to cookies.json")
    page.quit()
    display.stop()

if __name__ == "__main__":
    main()
