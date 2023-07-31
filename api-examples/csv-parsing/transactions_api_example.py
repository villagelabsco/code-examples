import requests
import csv

VILLAGE_API = "https://api-ledger.villagelabs.net"
USER_NETWORK = "<NETWORK ID PASTED HERE>"
BEARER_TOKEN = "<API KEY PASTED HERE>"
FILE_NAME = "<CSV FILE NAME HERE>"


def post_activity(body):
    url = f"{VILLAGE_API}/networks/{USER_NETWORK}/activity"
    headers = {"Authorization": "Bearer " + BEARER_TOKEN}
    response = requests.post(url, headers=headers, json=body)
    return response


with open(FILE_NAME, newline='') as csvfile:
    csvreader = csv.DictReader(csvfile)

    for i, row in enumerate(csvreader, 1):
        print(f"Reading row {i}/{csvreader.line_num}")

        usersKey = row["user_1_key"]
        userEmail = row["user_1_email"]
        amount = str(row["amount"])  # Must be string
        activityID = row["activity_short_id"]
        timestamp = int(row["activity_timestamp"])
        description = row["description"]
        reference = row["reference"]
        allowUnknown = True
        message = {
            "activity_short_id": activityID,
            "amount": amount,
            "users": {
                usersKey: userEmail,
            },
            "metadata": {
                "description": description,
                "activity_timestamp": timestamp,
                "reference": reference,
            },
        }

        response = post_activity(message)
        if response.status_code == 200:
            print(f"Transaction executed successfully: {reference}")
        else:
            print(
                f"Transaction executed failed for {reference}: {response.json()}")
