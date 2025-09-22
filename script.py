from bs4 import BeautifulSoup
import urllib.parse
import time
import json
import traceback
import os
import sys
import requests
from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage._elements.none_element import NoneElement
from DrissionPage._elements.chromium_element import ChromiumElement
try:
    from pyvirtualdisplay import Display
    use_display = True
except:
    use_display = False

QUERY = "test"

def run_script(knitsail, script):
    if use_display:
        display = Display(visible=0, size=(1920, 1080))
        display.start()

    options = ChromiumOptions()
    options.set_argument('--no-sandbox')
    options.set_argument('--disable-dev-shm-usage')
    options.headless(False)

    page = ChromiumPage(options)
    page.set.user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36")
    page.get('https://www.google.com/')

    page.run_js(knitsail)
    result = page.run_js(script)

    if use_display:
        display.stop()
    
    return result

def solve_captcha(sitekey, s, cookies):
    if not apikey:
        raise Exception("API key is required")
    task = requests.post("https://api.capmonster.cloud/createTask", json={
        "clientKey": apikey,
        "task": {
            "type": "RecaptchaV2EnterpriseTask",
            "websiteURL": "https://www.google.com/sorry/index",
            "websiteKey": sitekey,
            "enterprisePayload": {
                "s": s
            },
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "proxyType": "http",
            "proxyAddress": "linode.voids.top",
            "proxyPort": 1080,
            "proxyLogin": "bruteforce",
            "proxyPassword": "sineyo",
            "cookies": cookies
        }
    }).json()
    task_id = task.get("taskId")
    if not task_id:
        raise Exception(task.get("errorDescription"))
    for _ in range(60):
        result = requests.get(f"https://api.capmonster.cloud/getTaskResult", json={
            "clientKey": apikey,
            "taskId": task_id
        }).json()
        if result.get("status") == "ready":
            return result.get("solution").get("gRecaptchaResponse")
        if result.get("errorId"):
            raise Exception(result.get("errorDescription"))
        time.sleep(1)
    raise Exception("Timeout")

def sg_ss(knitsail, p, q):
    script = """
    var f = function(a) {
        var b = 0;
        return function() {
            return b < a.length ? {
            done: !1,
            value: a[b++]
            } : {
            done: !0
            }
        }
    };

    var l = function(a) {
        var b = typeof Symbol != "undefined" && Symbol.iterator && a[Symbol.iterator];
        if (b) return b.call(a);
        if (typeof a.length == "number") return {
            next: f(a)
        };
        throw Error("a`" + String(a));
    };

    var a = l(knitsail.a("<p>", function(){}, false)).next().value;
    var q = "<query>";
    return a([{q}]);
    """.replace("<p>", p).replace("<query>", urllib.parse.quote(q))
    return run_script(knitsail, script)

def main():
    session = requests.Session()
    session.headers = {
        #'authority': 'www.google.com',
        #'accept': '*/*',
        #'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        #'accept-language': 'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7',
        #'accept-encoding': 'br',
        #'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://www.google.com/',
        'sec-ch-ua': '"Chromium";v="137", "Not:A-Brand";v="24", "Google Chrome";v="137"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    }
    session.proxies = {
        "http": proxy,
        "https": proxy
    }
    response = session.get(f"https://www.google.com/search", params={"q": QUERY})
    soup = BeautifulSoup(response.text, "html.parser")
    knitsail = soup.find_all("script")[2].get_text()
    p = response.text.split("var p='")[1].split("'")[0]
    eid = response.text.split("var eid='")[1].split("'")[0]
    session.cookies.update({"SG_SS": sg_ss(knitsail, p, QUERY)})
    result = session.get(f"https://www.google.com/search", params={"q": QUERY, "sei": eid}, headers={"referer": f"https://www.google.com/search?q={QUERY}"})
    while "captcha-form" in result.text:
        soup = BeautifulSoup(result.text, "html.parser")
        payload = {
            "g-recaptcha-response": solve_captcha(soup.find("div", {"id": "recaptcha"}).get("data-sitekey"), soup.find("div", {"id": "recaptcha"}).get("data-s"), "; ".join([f"{name}={value}" for name, value in session.cookies.get_dict().items()])),
            "q": soup.find("input", {"name": "q"}).get("value"),
            "continue": soup.find("input", {"name": "continue"}).get("value")
        }
        result = session.post("https://www.google.com/sorry/index", data=payload)
    if "knitsail" in result.text:
        raise Exception("Failed to solve knitsail")
    else:
        print("possible done")
        open("cookies.json", "w", encoding="utf_8").write(json.dumps(session.cookies.get_dict(), ensure_ascii=False))
        open("result.html", "w", encoding="utf_8").write(result.text)

if __name__ == "__main__":
    try:
        proxy = sys.argv[1]
    except:
        proxy = None
    try:
        apikey = sys.argv[2]
    except:
        apikey = None
    for n in range(5):
        try:
            main()
            break
        except:
            traceback.print_exc()
        if n == 4:
            raise Exception("Failed to get cookies after 5 attempts")
