import os
import requests
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WABA_ID = "987593120853194"

url = f"https://graph.facebook.com/v22.0/{WABA_ID}/subscribed_apps"
headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}

response = requests.post(url, headers=headers)
print(response.status_code, response.text)