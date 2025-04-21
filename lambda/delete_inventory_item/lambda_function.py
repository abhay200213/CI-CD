import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    item_id = event.get('pathParameters', {}).get('id')
    if not item_id:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": "No item ID provided"})
        }

    response = table.query(
        KeyConditionExpression=Key('id').eq(item_id)
    )
    items = response.get('Items', [])
    if not items:
        return {
            "statusCode": 404,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": "Item not found"})
        }

    item_to_delete = items[0]
    table.delete_item(Key={
        "id": item_to_delete["id"],
        "location_id": item_to_delete["location_id"]
    })

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps({"message": f"Item {item_id} deleted"})
    }
