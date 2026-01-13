from access_token import refresh_access_token
import requests
import os
import time
from datetime import datetime, timezone


def lambda_handler(event, context):

    ACCESS_TOKEN = refresh_access_token()
    withings_url = 'https://wbsapi.withings.net/measure'
    end_date = int(time.time())
    start_date = end_date - 86400
    

    withings_data = {
        'action': 'getmeas',
        'meastype': 1,
        'category': 1,
        'startdate': start_date,
        'enddate': end_date
        
    
    }

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    withings_response = requests.post(withings_url, data=withings_data, headers=headers).json()

    weight = (withings_response["body"]["measuregrps"][0]["measures"][0]["value"] / 1000)
    date_str = datetime.fromtimestamp(end_date, tz=timezone.utc).strftime('%Y-%m-%d')


    INTERVALS_API_KEY = os.environ['INTERVALS_API_KEY']
    INTERVALS_ID = os.environ['INTERVALS_ID']
    intervals_url =  f"https://intervals.icu/api/v1/athlete/{INTERVALS_ID}/wellness/{date_str}"
    intervals_response = requests.put(intervals_url, json = {"weight": weight}, auth = ("API_KEY", INTERVALS_API_KEY))

    return (intervals_response.status_code)
