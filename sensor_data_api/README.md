# Sensor Data API

This folder contains two AWS Lambda functions for managing sensor data in a DynamoDB-backed system. These functions are designed to work with IoT or environmental monitoring applications that send structured sensor payloads.

## Overview

The functions in this folder perform the following tasks:

1. **store_sensor_data.py**  
   Accepts incoming JSON payloads containing sensor readings, validates and parses them, and stores the readings in DynamoDB using a composite key format:
   - `device_id` as the partition key (prefixed with `device#`)
   - `timestamp` as the sort key (prefixed with `ts#<epoch_millis>_<type>`)

2. **get_latest_readings.py**  
   Queries the most recent 50 records for a given device and returns the latest reading for each `sensor_type`. Useful for UI dashboards or status polling endpoints.

---

## File Descriptions

| File                   | Purpose                                            |
|------------------------|----------------------------------------------------|
| `store_sensor_data.py` | Ingests and writes structured sensor data to DynamoDB |
| `get_latest_readings.py` | Retrieves the latest readings for each sensor type for a given device |

---

## Requirements

- Python 3.9+
- AWS Lambda-compatible deployment
- IAM role with permission to access the target DynamoDB table

---

## DynamoDB Schema Assumptions

- Table has partition key `device_id` and sort key `timestamp`
- `timestamp` format: `ts#<epoch_millis>_<sensor_type>`
- Other stored attributes: `organization_id`, `thing_name`, `sensor_type`, `value`, `unit`, `event_timestamp`

---

## Example Payload (for `store_sensor_data.py`)

```json
{
  "company": { "id": "org123" },
  "location": { "id": "loc456" },
  "device_type": { "model": "sensorA" },
  "device": { "thing_name": "Fridge A" },
  "event_data": {
    "device_id": "abc123",
    "payload": [
      {
        "type": "temp",
        "value": 4.2,
        "unit": "C",
        "timestamp": 1722367245000
      },
      {
        "type": "rel_hum",
        "value": 33.1,
        "unit": "%",
        "timestamp": 1722367245000
      }
    ]
  }
}
