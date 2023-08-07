import boto3
import csv
import os

kinesis_client = boto3.client('kinesis')
kinesis_stream_name = "Test_Demo_Data_Stream"

def lambda_handler(event, context):
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        object_key = "Syntesis Matrix.csv"
        # ÷\record['s3']['object']['key']
        print("bucketname",bucket_name)
        print("object_key",object_key)

        csv_data = get_csv_data(bucket_name, object_key)
        # print("data into s3",csv_data)
        put_records_into_kinesis(csv_data)

def get_csv_data(bucket_name, object_key):
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    return response['Body'].read().decode('utf-8')

def put_records_into_kinesis(csv_data):
    csv_reader = csv.reader(csv_data.splitlines())
    for row in csv_reader:
        record_data = ','.join(row)  # Adjust if your CSV has different delimiters
        response = kinesis_client.put_record(
            StreamName=kinesis_stream_name,
            Data=record_data,
            PartitionKey=str(hash(record_data))  # Using a hash as the partition key
        )
        print("Record put into Kinesis stream:", response['SequenceNumber'])