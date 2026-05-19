import re,requests

print(re.findall(
    '\[null,1,\[null,null,5,null,"([^"]+)",null,"([^"]+)"\],\["([^"]+)","([^"]+)","([^"]+)"',
    requests.get(
        "https://www.google.com/search?q=github",
        headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'},
        cookies={cookie["name"]: cookie["value"] for cookie in requests.get("https://raw.githubusercontent.com/kino-tkr/google-cookie-autogen/refs/heads/main/cookies.json").json()}
    ).text
))
