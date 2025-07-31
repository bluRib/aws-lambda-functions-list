import boto3
from boto3.dynamodb.conditions import Key
import json
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TABLE_NAME')

def lambda_handler(event, context):
    print("Incoming event:")
    print(json.dumps(event, indent=2))

    query_params = event.get('queryStringParameters') or {}
    device_id = query_params.get('device_id')

    if not device_id:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': 'device_id query param is required'})
        }

    try:
        response = table.query(
            KeyConditionExpression=Key('device_id').eq(device_id),
            ScanIndexForward=False,  # newest first
            Limit=50
        )

        items = response.get('Items', [])
        print(f"Retrieved {len(items)} items for device_id={device_id}")

        latest_readings = {}
        thing_name = None

        for item in items:
            sensor_type = item.get('sensor_type')

            if not thing_name:
                thing_name = item.get('thing_name')

            if sensor_type and sensor_type not in latest_readings:
                value = item.get('value')
                if isinstance(value, Decimal):
                    value = float(value)

                latest_readings[sensor_type] = {
                    'value': value,
                    'unit': item.get('unit'),
                    'timestamp': item.get('timestamp')
                }

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'device_id': device_id,
                'thing_name': thing_name,
                'readings': latest_readings
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        }
