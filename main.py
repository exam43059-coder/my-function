import json
import os
import urllib.request
from datetime import datetime, timezone

BASE = os.environ.get("NAME", "USD").upper()  # базовая валюта, по умолчанию USD
TARGETS = ["KZT", "EUR", "RUB", "GBP", "CNY"]

url = f"https://open.er-api.com/v6/latest/{BASE}"

try:
    with urllib.request.urlopen(url, timeout=15) as resp:
        data = json.load(resp)
except Exception as e:
    print(f"Ошибка запроса: {e}")
    raise SystemExit(1)

if data.get("result") != "success":
    print(f"API вернул ошибку: {data}")
    raise SystemExit(1)

rates = data["rates"]
now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

print(f"Курсы валют на {now}")
print(f"1 {BASE} =")
for cur in TARGETS:
    if cur in rates and cur != BASE:
        print(f"  {rates[cur]:.2f} {cur}")
