import json
import boto3
from decimal import Decimal
from datetime import datetime, timezone

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = dynamodb.Table('TABLE_NAME')

def lambda_handler(event, context):
    print("=== START ===")
    print("RAW EVENT:")
    print(json.dumps(event, indent=2))

    try:
        if not event.get("body"):
            print("No body field in event.")
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing body in request'})
            }

        body = json.loads(event['body'])
        print("Parsed body:")
        print(json.dumps(body, indent=2))

        event_data = body.get('event_data', {})
        company = body.get('company', {})
        location = body.get('location', {})
        device_type = body.get('device_type', {})
        device = body.get('device', {})

        device_id = event_data.get('device_id', 'unknown')
        org_id = str(company.get('id', 'unknown'))
        location_id = str(location.get('id', 'unknown'))

        print("company.id:", company.get("id"))
        print("device_id:", device_id)

        for reading in event_data.get('payload', []):
            ts = int(reading['timestamp'])  # Epoch millis
            ts_iso = datetime.fromtimestamp(ts / 1000, tz=timezone.utc).isoformat()

            composite_device_id = f"device#{device_id}"
            timestamp = f"ts#{reading['timestamp']}_{reading['type']}"

            TABLE_NAME.put_item(Item={
                'device_id': composite_device_id,
                'timestamp': timestamp,
                'organization_id': org_id,
                'thing_name': device.get('thing_name'),
                'sensor_type': reading.get('type'),
                'value': Decimal(str(reading.get('value'))),
                'unit': reading.get('unit'),
                'event_timestamp': ts,
            })

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Data was stored successfully'})
        }

    except Exception as e:
        print("Exception caught:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
