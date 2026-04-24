import requests, csv, os
from datetime import datetime

url = "https://hrtagold.id/api/v1/brandings/price/daily"
headers = {"Referer": "https://hrtagold.id/en/gold-price", "Accept": "application/json"}

r = requests.get(url, headers=headers, timeout=10)
data = r.json()

file_exists = os.path.exists("gold_history.csv")
with open("gold_history.csv", "a", newline="") as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["tanggal", "series", "gramasi", "harga_jual", "harga_buyback"])
    for series in data["data"]:
        for p in series["prices"]:
            writer.writerow([
                data["updated_date"][:10],
                series["series"],
                p["gramasi"],
                p["price"],
                p["buyback_price"]
            ])

print("Selesai:", data["updated_date"])
