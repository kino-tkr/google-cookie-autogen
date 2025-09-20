import random
import sys

tinyproxy_template = """Port 8888
Listen 127.0.0.1
Timeout 600
Allow 127.0.0.1
Upstream http {}
LogLevel Info"""

proxy = sys.argv[1]
proxy = proxy.replace(":1080", f":{random.randint(1080, 1380)}")
open("tinyproxy.conf", "w", encoding="utf_8").write(tinyproxy_template.format(proxy))
