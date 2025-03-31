from playwright.sync_api import sync_playwright
import json

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto('https://www.google.com/search?q=a')

        cookies = context.cookies()
        with open('cookies.json', 'w') as f:
            json.dump(cookies, f, indent=2)

        print("Cookies saved to cookies.json")
        browser.close()

if __name__ == "__main__":
    main()
