from flask import Flask, request
import os
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(override=True)

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

gemini_client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = (
    "Eres un asistente virtual de atención al cliente para un negocio local. "
    "Respondes de forma amable, breve y profesional, en español."
)


@app.route("/", methods=["GET"])
def home():
    return "Bot activo ✅"


@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Token inválido", 403

    data = request.get_json()
    print("Mensaje recibido:", data)

    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]

        if "messages" in value:
            message = value["messages"][0]
            from_number = message["from"]
            text = message["text"]["body"]

            print(f"Mensaje de {from_number}: {text}")

            respuesta_ia = ask_gemini(text)
            send_message(from_number, respuesta_ia)

    except (KeyError, IndexError) as e:
        print("Sin mensaje nuevo o error:", e)

    return "OK", 200


def ask_gemini(text):
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=text,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )
    return response.text


def send_message(to, text):
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    response = requests.post(url, headers=headers, json=payload)
    print("Respuesta de envío:", response.status_code, response.text)


if __name__ == "__main__":
    app.run(debug=True, port=5000)