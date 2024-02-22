from django.conf import settings
import requests
import os

def send_sms(phone_number, message):
    print("Sending SMS to:", phone_number)
    print("SMS Content:", message)

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
        response.raise_for_status()
        response_data = response.json()
        print("SMS Sent Successfully")
        return response_data
    except requests.exceptions.HTTPError as e:
        print("Failed to send SMS:", e)
        return None
    except Exception as e:
        print("An error occurred while sending SMS:", str(e))
        return None
