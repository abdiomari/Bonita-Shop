import requests
from requests.auth import HTTPBasicAuth

url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
auth = HTTPBasicAuth("YOUR_CONSUMER_KEY", "YOUR_CONSUMER")
response = requests.get(url, auth=auth)
access_token = response.json()['access_token']


url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
headers = {
    "Authorization": "Bearer %s" % access_token
}

request = {
    "ShortCode": "YOUR_SHORTCODE",
    "ResponseType": "Completed",
    "ConfirmationURL": "https://ip_address:port/confirmation",
    "ValidationURL": "https://ip_address:port/validation_url"
}

response = requests.post(url, json=request, headers=headers)
headers = {
    "Authorization": "Bearer %s" % access_token
}

request = {
    "ShortCode": "YOUR_SHORTCODE",
    "CommandID": "CustomerPayBillOnline",
    "Amount": "100",
    "Msisdn": "254708374149",
    "BillRefNumber": "TestAPI"
}

response = requests.post(url, json=request, headers=headers)
print(response.json())