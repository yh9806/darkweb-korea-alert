import json
import os
import requests
from datetime import datetime

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

POSTS_PATH = "ransomwatch/data/posts.json"
KOREAN_KEYWORDS = [".kr", "korea", "대한민국", "서울", "삼성", "카카오", "네이버", "lg", "sk", "한화", "현대", "롯데"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    print("텔레그램 응답:", response.text)

def is_korea_related(text):
    text = text.lower()
    return any(keyword.lower() in text for keyword in KOREAN_KEYWORDS)

def format_korea_alert(post):
    now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    message = (
        f"🎌 한국 관련 유출 감지 🎌\n\n"
        f"🦠 그룹: {post['group']}\n"
        f"🏢 대상: {post['title']}\n"
        f"🔗 링크: {post['url']}\n"
        f"🕒 감지 시간: {now_str}"
    )
    return message

def main():
    with open(POSTS_PATH, "r") as f:
        posts = json.load(f)

    for post in posts:
        text = post["title"] + " " + post["group"]
        if is_korea_related(text):
            msg = format_korea_alert(post)
            send_telegram(msg)

    print("한국 키워드 감지 완료")

if __name__ == "__main__":
    main()