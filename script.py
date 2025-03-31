from playwright.sync_api import sync_playwright
from pyvirtualdisplay import Display
import json
import time

def main():
    # 仮想ディスプレイを起動
    display = Display(visible=0, size=(1920, 1080))
    display.start()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto('https://www.google.com/search?q=a')
        time.sleep(5)  # ページ読み込みを待つ

        cookies = context.cookies()
        with open('cookies.json', 'w') as f:
            json.dump(cookies, f, indent=2)

        print("Cookies saved to cookies.json")
        browser.close()

    display.stop()

if __name__ == "__main__":
    main()
