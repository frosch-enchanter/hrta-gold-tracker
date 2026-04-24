import requests, csv, os

url = "https://hrtagold.id/api/v1/brandings/price/daily"
headers = {"Referer": "https://hrtagold.id/en/gold-price", "Accept": "application/json"}

r = requests.get(url, headers=headers, timeout=10)
data = r.json()
tanggal_update = data["updated_date"]

# Cek apakah tanggal ini sudah pernah disimpan
sudah_ada = False
if os.path.exists("gold_history.csv"):
    with open("gold_history.csv", "r") as f:
        for baris in f:
            if tanggal_update[:19] in baris:  # cek sampai detik
                sudah_ada = True
                break

if sudah_ada:
    print("Harga belum berubah, skip:", tanggal_update)
else:
    file_exists = os.path.exists("gold_history.csv")
    with open("gold_history.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["tanggal_update", "series", "gramasi", "harga_jual", "harga_buyback"])
        for series in data["data"]:
            for p in series["prices"]:
                writer.writerow([
                    tanggal_update,
                    series["series"],
                    p["gramasi"],
                    p["price"],
                    p["buyback_price"]
                ])
    print("Tersimpan:", tanggal_update)
