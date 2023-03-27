import requests
import time
import os

DELAY: int = 5 * 3600 # 5 hours

URL: str = "https://dashboard.honeygain.com/api/v1/contest_winnings"

def get_headers(token: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Authorization": "Bearer {}".format(token),
        "Origin": "https://dashboard.honeygain.com",
        "Connection": "keep-alive",
        "Referer": "https://dashboard.honeygain.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Content-Length": "0",
        "TE": "trailers"
    }
    return headers

def get_token(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def claim_honeypot(url: str, headers: str) -> int:
    response: requests.Response = requests.post(url, data="", headers=headers)
    if response.status_code != 200:
        print(response.text)
        return 0
    try:
        credits = response.json()["data"]["credits"]
        print(f"Received {credits} credits")
        return int(credits)
    except Exception as e:
        print(e)
    return 0

def main():
    total_credits_received: int = 0
    TOKEN: str = get_token("token.txt")
    HEADERS: dict = get_headers(TOKEN)
    while True:
        total_credits_received += claim_honeypot(URL, HEADERS)
        try:
            os.system(f"title Claimed so far: {total_credits_received} credits (${total_credits_received / 1000:.2f})")
        except Exception:
            print("Couldn't update console title because you are not running Windows")
        time.sleep(DELAY)

if __name__ == "__main__":
    main()