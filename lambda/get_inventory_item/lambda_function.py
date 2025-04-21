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

    item = items[0]
    if 'qty_on_hand' in item:
        item['qty_on_hand'] = int(item['qty_on_hand'])
    if 'price' in item:
        item['price'] = float(item['price'])

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps(item)
    }
