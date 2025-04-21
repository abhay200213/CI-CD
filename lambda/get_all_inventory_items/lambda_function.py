import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    response = table.scan()
    items = response.get('Items', [])
    for item in items:
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
        "body": json.dumps(items)
    }
