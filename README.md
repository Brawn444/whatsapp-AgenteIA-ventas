# Agente de IA para WhatsApp: atención al cliente y pedidos

Prototipo funcional de un agente conversacional para WhatsApp que atiende a los clientes de un negocio: muestra el menú, responde preguntas sobre horarios y precios, y toma pedidos confirmando el total a pagar. Usa la API de WhatsApp de Meta y Gemini (Google) para generar las respuestas.

Incluye un restaurante de ejemplo ("El Sabor Costeño"), pero los datos del negocio son configurables.

## Qué hace

- Recibe los mensajes de los clientes por WhatsApp mediante un webhook.
- Responde con IA (Gemini) de forma coherente, amable y en español.
- Mantiene la memoria de la conversación de cada cliente.
- Responde con la información real del negocio (menú, precios, horario) y evita inventar datos.
- Toma el pedido, pregunta la dirección de entrega y confirma el total.
- Cuando no sabe algo, lo dice y avisa que un encargado se comunicará.

## Tecnologías

- Python
- Flask (servidor del webhook)
- API de WhatsApp Cloud de Meta (Graph API)
- Gemini API (`gemini-2.5-flash`)
- requests, python-dotenv

## Cómo funciona

1. Meta envía cada mensaje del cliente al endpoint `/webhook`.
2. `app.py` obtiene (o crea) la sesión de chat de ese cliente con Gemini.
3. Gemini responde usando las instrucciones y el menú que genera `negocio.py`.
4. La respuesta se envía de vuelta al cliente por la API de WhatsApp.

## Estructura del proyecto

```
├── app.py          # Servidor Flask, webhook, conexión con Gemini y envío de mensajes
├── negocio.py      # Datos del negocio (menú, horario) y generación de las instrucciones de la IA
├── subscribe.py    # Suscribe la app a la cuenta de WhatsApp Business (se ejecuta una vez)
├── requirements.txt
├── .env.example
└── LICENSE         # Licencia MIT
```

Para usarlo con otro negocio solo hay que crear otro objeto `Negocio` en `negocio.py` con su nombre, horario, dirección y menú.

## Cómo ejecutarlo

1. Clona el repositorio e instala las dependencias:

```bash
git clone https://github.com/Brawn444/whatsapp-AgenteIA-ventas.git
cd whatsapp-AgenteIA-ventas
python -m venv venv
venv\Scripts\activate        # En Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

2. Copia `.env.example` a `.env` y completa las variables:

```
VERIFY_TOKEN=       # Token que tú eliges para verificar el webhook
WHATSAPP_TOKEN=     # Token de acceso de la API de WhatsApp (Meta for Developers)
PHONE_NUMBER_ID=    # ID del número de WhatsApp de prueba o producción
GEMINI_API_KEY=     # API key de Google AI Studio
WABA_ID=            # ID de la cuenta de WhatsApp Business
```

3. Inicia el servidor:

```bash
python app.py
```

4. Expón el servidor con una URL pública HTTPS (por ejemplo con ngrok) y configura en Meta for Developers el webhook con la URL `https://tu-url/webhook` y tu `VERIFY_TOKEN`.

5. Suscribe la app a tu cuenta de WhatsApp Business (solo la primera vez):

```bash
python subscribe.py
```

## Alcance y próximas mejoras

Es una demo funcional pensada para mostrar el flujo completo de un agente de ventas por WhatsApp. Por decisión de alcance **no usa base de datos todavía**: la memoria de las conversaciones vive en el programa y se reinicia con el servidor.

Ya incluye:

- [x] Manejo de errores cuando falla la API de Gemini o de WhatsApp (mensaje de respaldo al cliente y registro del error).
- [x] Respuesta a mensajes que no son de texto (imágenes, audios).
- [x] Procesamiento de varios mensajes en un mismo evento del webhook.
- [x] Registro con `logging`, sin exponer el contenido de las conversaciones.

Siguiente paso planeado:

- [ ] Persistencia con SQLite: guardar conversaciones y pedidos en una base de datos (tablas `mensajes` y `pedidos`), para que la memoria no se pierda al reiniciar el servidor.

Para llevarlo a producción también haría falta:

- [ ] Calcular el total del pedido en el código y no solo con las instrucciones del modelo.
- [ ] Validar la firma de los mensajes que llegan de Meta.
- [ ] Transcribir audios y soportar imágenes.

## Autor

Gustavo Andrés Camelo Vásquez, estudiante de Tecnología en Análisis y Desarrollo de Software (SENA).
