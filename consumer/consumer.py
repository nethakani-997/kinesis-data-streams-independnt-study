import base64
import csv

def lambda_handler(event, context):
    for record in event['Records']:
        # Decode the base64-encoded data in the record
        payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        
        # Split the CSV data into rows
        csv_rows = payload.split('\n')
        
        # Process each row
        for row in csv_rows:
            process_csv_row(row)

def process_csv_row(row):
    # Parse the CSV row
    csv_values = row.split(',')
    
    # Do whatever processing you need with the CSV values
    print("CSV values:", csv_values)