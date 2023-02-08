import csv
import requests

VILLAGE_API = "https://api-server-z6lqdoyzpq-uc.a.run.app"
USER_NETWORK = "<ENTER_YOUR_NETWORK>"
BEARER_TOKEN = "<ENTER_YOUR_GENERATED_API_KEY>"
SALES_INCENTIVE_CLASS = "<ENTER_YOUR_SALES_INCENTIVE>"

def post_transaction(buyer, seller, amount, denom, ref, productClass, ts, description, allowUnknown):
    url = f"{VILLAGE_API}/networks/{USER_NETWORK}/transactions"
    headers = {"Authorization": "Bearer " + BEARER_TOKEN}
    payload = [{"buyer": buyer, "seller": seller, "amount": amount, "denom": denom, "ref": ref, "productClass": productClass, "ts": ts, "description": description, "allowUnknown": allowUnknown}]
    response = requests.post(url, headers=headers, json=payload)
    return response

with open("transactions.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        buyer = row["buyer"]
        seller = row["seller"]
        amount = float(row["amount"])
        denom = row["denom"]
        ref = row["ref"]
        productClass = SALES_INCENTIVE_CLASS
        ts = int(row["ts"])
        description = row["description"]
        allowUnknown = True

        response = post_transaction(buyer, seller, amount, denom, ref, productClass, ts, description, allowUnknown)
        if response.status_code == 200:
            print(f"Transaction executed successfully: {ref}")
        else:
            print(f"Transaction executed failed for {ref}: {response.json()}")
