import requests

url = "https://www.smart2trader.com/api/tiago_iq_asset_alert/GetAssets.php"

r = requests.get(url)

json = r.json()

for i in range(0, len(json["msg"])):
    print(json["msg"][i]["name"])

#print(json["msg"][0]["name"])