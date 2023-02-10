import csv
import requests
import time

VILLAGE_API = "https://api-server-u2blzhjdqa-uc.a.run.app"
USER_NETWORK = "<ENTER_YOUR_NETWORK>"
BEARER_TOKEN = "<ENTER_YOUR_GENERATED_API_KEY>"
# SALES_INCENTIVE_CLASS = "<ENTER_YOUR_SALES_INCENTIVE>"    # Optional, only required if your network has more than 1 sales incentive class.
BATCH_SIZE = 3

def post_transaction(batch):
    url = f"{VILLAGE_API}/networks/{USER_NETWORK}/transactions"
    headers = {"Authorization": "Bearer " + BEARER_TOKEN}
    response = requests.post(url, headers=headers, json=batch)
    return response

with open("transactions.csv") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    total_rows = len(rows)
    batch = []
    for i, row in enumerate(rows):
        print("Reading row %d/%d" % (i + 1, total_rows))
        buyer = row["buyer"]
        seller = row["seller"]
        amount = float(row["amount"])
        denom = row["denom"]
        ref = row["ref"]
        productClass = SALES_INCENTIVE_CLASS
        ts = int(row["ts"])
        description = row["description"]
        allowUnknown = True
        batch.append({"buyer": buyer, "seller": seller, "amount": amount, "denom": denom, "ref": ref, "ts": ts, "description": description, "allowUnknown": allowUnknown})
        if len(batch) >= BATCH_SIZE or i == total_rows - 1:
            print("Submitting batch of " + str(len(batch))+  "...")
            response = post_transaction(batch)
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
        
        
            
    
