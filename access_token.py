import json
import boto3
from botocore.exceptions import ClientError
import requests
import os

request_url = "https://wbsapi.withings.net/v2/oauth2"
secret_name = "withings/token"
region_name = "us-east-1"
session = boto3.session.Session()
client = session.client(
    service_name='secretsmanager',
    region_name=region_name
)

def refresh_access_token():

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    REFRESH_TOKEN = json.loads(get_secret_value_response['SecretString'])["REFRESH_TOKEN"]
    CLIENT_ID = os.environ["CLIENT_ID"]
    CLIENT_SECRET = os.environ["CLIENT_SECRET"]

    payload = {
        "action": "requesttoken",
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN
        
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(request_url, data=payload, headers=headers).json()
    ACCESS_TOKEN = response["body"]["access_token"]
    REFRESH_TOKEN = response["body"]["refresh_token"]

    
    client.put_secret_value(
        SecretId=secret_name,
        SecretString=json.dumps({"REFRESH_TOKEN": REFRESH_TOKEN})
    )

    return (ACCESS_TOKEN)
