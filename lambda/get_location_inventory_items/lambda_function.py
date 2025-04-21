import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    loc_id = event.get('pathParameters', {}).get('id')
    if not loc_id:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": "No location ID provided"})
        }

    try:
        loc_id_int = int(loc_id)
    except ValueError:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": "Invalid location ID"})
        }

    response = table.query(
        IndexName="LocationIndex",  # match the index name you gave
        KeyConditionExpression=Key('location_id').eq(loc_id_int)
    )
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
