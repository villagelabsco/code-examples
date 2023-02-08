import csv
import requests

VILLAGE_API = "https://api-server-z6lqdoyzpq-uc.a.run.app"
USER_NETWORK = "<ENTER_YOUR_NETWORK>"
BEARER_TOKEN = "<ENTER_YOUR_GENERATED_API_KEY>"

def post_work(userId, workTypeId, amount, ref, ts, description, allowUnknown):
    url = f"{VILLAGE_API}/networks/{USER_NETWORK}/work"
    headers = {"Authorization": "Bearer " + BEARER_TOKEN}
    payload = [{"userId": userId, "workTypeId": workTypeId, "amount": amount, "ref": ref, "ts": ts, "description": description, "allowUnknown": allowUnknown}]
    response = requests.post(url, headers=headers, json=payload)
    return response

with open("work.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        buyer = row["userId"]
        workTypeId = row["workTypeId"]
        amount = float(row["amount"])
        ref = row["ref"]
        ts = int(row["ts"])
        description = row["description"]
        allowUnknown = True

        response = post_work(buyer, workTypeId, amount, ref, ts, description, allowUnknown)
        if response.status_code == 200:
            print(f"Transaction executed successfully: {ref}")
        else:
            print(f"Transaction executed failed for {ref}: {response.json()}")
