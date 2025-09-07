import requests
import json

url = "https://api2.bybit.com/fiat/otc/config/getTokenList"
resp = requests.get(url)
data = resp.json()

print(json.dumps(data, indent=2, ensure_ascii=False))
