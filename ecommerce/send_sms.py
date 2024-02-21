from django.conf import settings
import requests
import os

"""
Function to send message in a seperate thread when order is sent
"""
def send_sms(phone_number, message):
    url = settings.AFRICASTALKING_URL
    username = settings.AFRICASTALKING_USERNAME
    api_key = settings.AFRICASTALKING_API_KEY
    sender_id = settings.AFRICASTALKING_SENDER_ID

    headers = {
        'ApiKey': api_key,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    data = {
        'username': username,
        'from': sender_id,
        'message': message,
        'to': phone_number
    }

    try:
        response = requests.post(url=url, headers=headers, data=data)
        response_data = response.json()
        if response.status_code == 201:
            return response_data
        else:
            return None
    except Exception as e:
        return None
