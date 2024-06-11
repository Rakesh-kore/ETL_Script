import boto3
import hashlib
import psycopg2
import json
from datetime import datetime

# Connect to localstack SQS
sqs = boto3.client('sqs', endpoint_url='http://localhost:4566', region_name='us-east-1')
queue_url = 'http://localhost:4566/000000000000/login-queue'

# Connect to Postgres
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Function to mask PII
def mask_pii(value):
    return hashlib.sha256(value.encode()).hexdigest()

# Function to process messages
def process_message(message):
    data = json.loads(message['Body'])

    user_id = data['user_id']
    device_type = data['device_type']
    masked_ip = mask_pii(data['ip'])
    masked_device_id = mask_pii(data['device_id'])
    locale = data['locale']
    app_version = int(data['app_version'].split('.')[0])
    create_date = datetime.strptime(data['create_date'], '%Y-%m-%d').date()

    return (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)

# Read messages from SQS
response = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=10,
    WaitTimeSeconds=5
)

if 'Messages' in response:
    for message in response['Messages']:
        record = process_message(message)
        cur.execute("""
            INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
            VALUES (%s, %s, %s, %s, %s, %d, %s)
            """, record)
        conn.commit()
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])

cur.close()
conn.close()
