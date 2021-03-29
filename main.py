import requests
import config
import os
from twilio.http.http_client import TwilioHttpClient
from twilio.rest import Client
MY_LAT = 12.971599
MY_LONG = 77.594566
auth_token=config.AUTH_TOKEN
account_sid=config.ACCOUNT_SID
api_key=config.OWM_API_KEY
parameters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "exclude":"current,minutely,daily",
    "appid": api_key}

it_will_rain = False
response = requests.get(url="https://api.openweathermap.org/data/2.5/onecall",params=parameters)
response.raise_for_status()
# print(response.status_code)
data = response.json()["hourly"]
weather_codes = []
for hour in data[:12]:
    code=hour["weather"][0]["id"]
    if code<700:
        it_will_rain=True
        break

if it_will_rain:
    print("Carry umbrella!")
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token,http_client=proxy_client)
    message = client.messages.create(
        body="It's going to rain today.\nCarry an umbrella ☔🌂 - Muskan",
        from_=config.twilio_phone_num,
        to=config.my_phone_num
    )
    print(message.status)
else:
    print("No need to carry umbrella!")

