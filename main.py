import json
import os
import urllib.request
from datetime import datetime, timezone

# Настройки
BASE = (os.environ.get("NAME") or "USD").upper()  # базовая валюта
TARGETS = ["KZT", "EUR", "RUB", "GBP", "CNY"]     # какие валюты показывать
TG_TOKEN = os.environ.get("TG_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")


def get_rates(base):
    url = f"https://open.er-api.com/v6/latest/{base}"
    with urllib.request.urlopen(url, timeout=15) as resp:
        data = json.load(resp)
    if data.get("result") != "success":
        raise RuntimeError(f"API вернул ошибку: {data}")
    return data["rates"]


def send_telegram(text):
    payload = json.dumps({"chat_id": TG_CHAT_ID, "text": text}).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    urllib.request.urlopen(req, timeout=15)


def main():
    try:
        rates = get_rates(BASE)
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        raise SystemExit(1)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [f"Курсы валют на {now}", f"1 {BASE} ="]
    for cur in TARGETS:
        if cur in rates and cur != BASE:
            lines.append(f"  {rates[cur]:.2f} {cur}")
    text = "\n".join(lines)

    print(text)

    if TG_TOKEN and TG_CHAT_ID:
        try:
            send_telegram(text)
            print("Отправлено в Telegram")
        except Exception as e:
            print(f"Не удалось отправить в Telegram: {e}")
            raise SystemExit(1)
    else:
        print("Telegram не настроен, отправка пропущена")


if __name__ == "__main__":
    main()
