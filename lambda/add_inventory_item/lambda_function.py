import json
import boto3
from decimal import Decimal
import ulid  # make sure ULID is added to deployment package if needed

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    try:
        data = json.loads(event.get('body', '{}'), parse_float=Decimal)
    except Exception:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": "Invalid JSON in request body"})
        }

    required_fields = ["name", "description", "qty_on_hand", "price", "location_id"]
    if any(field not in data for field in required_fields):
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": "Missing required fields"})
        }

    item_id = str(ulid.new())

    new_item = {
        "id": item_id,
        "name": data["name"],
        "description": data["description"],
        "qty_on_hand": int(data["qty_on_hand"]),
        "price": Decimal(str(data["price"])),
        "location_id": int(data["location_id"])
    }

    table.put_item(Item=new_item)
    new_item["price"] = float(new_item["price"])

    return {
        "statusCode": 201,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps(new_item)
    }
