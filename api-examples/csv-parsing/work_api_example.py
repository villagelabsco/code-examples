import csv
import requests
import time

VILLAGE_API = "https://api-server-u2blzhjdqa-uc.a.run.app"
USER_NETWORK = "<ENTER_YOUR_NETWORK>"
BEARER_TOKEN = "<ENTER_YOUR_GENERATED_API_KEY>"
BATCH_SIZE = 3

def post_work(batch):
    url = f"{VILLAGE_API}/networks/{USER_NETWORK}/work"
    headers = {"Authorization": "Bearer " + BEARER_TOKEN}
    response = requests.post(url, headers=headers, json=batch)
    return response

with open("work.csv") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    total_rows = len(rows)
    batch = []
    for i, row in enumerate(rows):
        print("Reading row %d/%d" % (i + 1, total_rows))
        buyer = row["userId"]
        workTypeId = row["workTypeId"]
        amount = float(row["amount"])
        ref = row["ref"]
        ts = int(row["ts"])
        description = row["description"]
        allowUnknown = True

        batch.append({"userId": buyer, "workTypeId": workTypeId, "amount": amount, "ref": ref, "ts": ts, "description": description, "allowUnknown": allowUnknown})
        if len(batch) >= BATCH_SIZE or i == total_rows - 1:
            print("Submitting batch of " + str(len(batch))+  "...")
            response = post_work(batch)
            if response.status_code == 200:
                print(f"Transaction executed successfully: {ref}")
            else:
                print(f"Transaction executed failed for {ref}: {response.json()}")
            
            if i < total_rows - 1:
                print("Waiting for next block...")
                batch.clear()
                time.sleep(5)
            else:
                print("Done!")
