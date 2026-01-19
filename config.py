import os
from urllib.parse import urljoin


class UserConfig:
    EMAIL = os.getenv("EMAIL") or ""
    PASSWORD = os.getenv("PASSWORD") or ""


TARGET_URL = os.getenv("TARGET_URL") or "https://www.sexyai.top/" # Meimodu官网，可更换为其他域名，如 https://www.meimoai8.com/


REQUEST_CONFIG = {
    "timeout": 10,
    # "retries": 3, # 设置重试次数似乎会导致 cloudscraper 处理挑战失败
    "headers": {
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Referer": TARGET_URL,
    }
}


API_CONFIG = {
    "base_url": urljoin(TARGET_URL, "/api"),
    "endpoints": {
        "login": "/user/login",
        "sign-in": "/user/sign-in",
        "info": "/user/info",
    }
}