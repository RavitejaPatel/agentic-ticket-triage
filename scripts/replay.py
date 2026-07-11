import csv
import time
import requests
import json
from datetime import datetime, timezone

API_URL = "http://localhost:8000/submit-ticket"
CSV_PATH = "data/tickets.csv"
LIMIT = 50  # start small; raise once confirmed working


def build_ticket_text(row: dict) -> str:
    description = row["Ticket Description"].replace(
        "{product_purchased}", row["Product Purchased"]
    )
    return f"{row['Ticket Subject']}. {description}"


def replay_tickets():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= LIMIT:
                break

            ticket_text = build_ticket_text(row)
            print(f"\n--- Ticket {i+1} ---")
            print(ticket_text[:150])

            response = requests.post(API_URL, json={"ticket_text": ticket_text})
            if response.status_code == 200:
                result = response.json()
                print("Classified as:", result["classification"])
                print("Routing:", result["routing_decision"]["action"])

                log_entry = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "ticket_text": ticket_text,
                    "classification": result["classification"],
                    "routing_decision": result["routing_decision"],
                    "kaggle_priority": row.get("Ticket Priority"),
                }
                with open("logs/ticket_log.jsonl", "a") as log_file:
                    log_file.write(json.dumps(log_entry) + "\n")
                
            else:
                print("ERROR:", response.status_code, response.text)

            time.sleep(0.5)  # be gentle on the Bedrock API rate limits


if __name__ == "__main__":
    replay_tickets()