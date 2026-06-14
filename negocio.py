class Negocio:
    def __init__(self, nombre, tipo, horario, direccion, telefono, menu):
        self.nombre = nombre
        self.tipo = tipo
        self.horario = horario
        self.direccion = direccion
        self.telefono = telefono
        self.menu = menu

    def generar_prompt(self):
        menu_texto = "\n".join(
            f"- {item['nombre']}: ${item['precio']:,} — {item['descripcion']}"
            for item in self.menu
        )

        return f"""Eres el asistente virtual de atención al cliente de "{self.nombre}", un {self.tipo} ubicado en {self.direccion}.

Información del negocio:
- Horario de atención: {self.horario}
- Teléfono: {self.telefono}

Menú disponible:
{menu_texto}

Instrucciones:
- Responde siempre en español, de forma amable, breve y profesional.
- Si el cliente pregunta por el menú, los precios o el horario, responde con la información exacta de arriba.
- Si el cliente quiere hacer un pedido, pregúntale qué platos quiere (solo del menú disponible) y su dirección de entrega. Cuando tengas ambos datos, confirma el pedido completo con el total a pagar, y dile que un encargado se pondrá en contacto para coordinar la entrega.
- Si preguntan algo que no sabes (ej. reservas para más de 10 personas, eventos especiales), dilo honestamente y ofrece que un encargado del restaurante se comunicará pronto.
- No inventes platos, precios ni horarios que no esten en esta informacion."""


restaurante_demo = Negocio(
    nombre="El Sabor Costeño",
    tipo="restaurante de comida típica costeña",
    horario="Lunes a sábado de 11:00 am a 9:00 pm, domingos de 11:00 am a 5:00 pm",
    direccion="Cra 15 #22-30, Soledad, Atlántico",
    telefono="300 123 4567",
    menu=[
        {"nombre": "Sancocho de gallina", "precio": 18000, "descripcion": "Con yuca, plátano y mazorca"},
        {"nombre": "Arroz con coco y camarones", "precio": 25000, "descripcion": "Servido con patacones"},
        {"nombre": "Pescado frito (mojarra)", "precio": 22000, "descripcion": "Con ensalada y patacón"},
        {"nombre": "Carimañolas (porción x3)", "precio": 8000, "descripcion": "Relleno de carne desmechada"},
        {"nombre": "Limonada de coco", "precio": 7000, "descripcion": "Refrescante, tamaño grande"},
        {"nombre": "Jugo natural", "precio": 5000, "descripcion": "Sabores: mango, maracuyá, guayaba"},
    ]
)