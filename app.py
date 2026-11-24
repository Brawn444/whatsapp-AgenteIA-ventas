from flask import Flask, request
import os
import logging
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types
from negocio import restaurante_demo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv(override=True)

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

gemini_client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = restaurante_demo.generar_prompt()
# Diccionario: numero_telefono -> sesion de chat con Gemini
conversaciones = {}


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

    data = request.get_json(silent=True) or {}

    try:
        value = data["entry"][0]["changes"][0]["value"]

        for message in value.get("messages", []):
            from_number = message["from"]

            if message.get("type") != "text":
                send_message(from_number, "Por ahora solo entiendo mensajes de texto 😊")
                continue

            text = message["text"]["body"]
            logger.info("Mensaje recibido de %s", from_number)

            try:
                respuesta_ia = ask_gemini(from_number, text)
            except Exception:
                logger.exception("Error al consultar Gemini")
                respuesta_ia = "Tuve un problema, ¿me repites por favor?"

            send_message(from_number, respuesta_ia)

    except (KeyError, IndexError):
        logger.info("Evento sin mensajes")

    return "OK", 200


def get_chat(from_number):
    """Devuelve la sesion de chat de este cliente, creando una nueva si no existe."""
    if from_number not in conversaciones:
        conversaciones[from_number] = gemini_client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT
            )
        )
    return conversaciones[from_number]


def ask_gemini(from_number, text):
    chat = get_chat(from_number)
    response = chat.send_message(text)
    return response.text or "No pude generar una respuesta, ¿me repites por favor?"


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
    if not response.ok:
        logger.error("Fallo al enviar mensaje: %s %s", response.status_code, response.text)


if __name__ == "__main__":
    app.run(debug=False, port=5000)
