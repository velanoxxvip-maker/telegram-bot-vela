import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURACIÓN ---
# Asegúrate de que estas variables estén configuradas en tu entorno de hosting (TOKEN y ADMIN_ID)
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# --- MENSAJES ---
MENSAJE_BIENVENIDA = """🌟 *Mensaje de bienvenida* 🌟

👋 ¡Hola amor! Soy *Vela Noxx* 💋
Bienvenid@ a mi espacio exclusivo 🔥.

Explora el menú aquí abajo 👇 y descubre todo lo que tengo preparado para ti ✨.
"""

MENSAJE_VIP = """💎 Suscripción VIP – Bs. 150 / mes 💎

👉 Con tu suscripción tendrás acceso inmediato al Canal VIP diamante 💎, donde encontrarás:
✨ TODO mi contenido explícito 🤯 y premium durante 1 mes completo.
🔥 Fotos + videos exclusivos.
💞 Acceso a lo más íntimo.
😈 Una experiencia única conmigo, sin censura.

📌 Acceso por 30 días al Canal VIP DIAMANTE con tu aporte de Bs. 150.

⚠ IMPORTANTE ⚠
Para activarlo debes enviarme:
⿡ Tu comprobante de pago 📸
⿢ Tu @usuario de Telegram (ejemplo: @juan23, @carlitos89).

🚫 Si no me mandas tu @usuario, me sales como “usuario desconocido” 🤖❌ y no podré enviarte tu link VIP.

👉 Si aún no tienes usuario, créalo en:
Configuración > Editar perfil > Nombre de usuario.
(Ejemplo: @pedro2025).
"""

MENSAJE_PROMOS = """Hola corazón 💕✨
Por el momento no tenemos promociones activas 😘.
Pero tranquila/o, cuando hayan promos 🔥 voy a estar avisando en mis canales:

👉 ZonaSecreta1
👉 ZonaSecreta2

Estaré esperando por ti 💋💌
"""

MENSAJE_SALIDAS = """🚫 *No realizo servicios* 🚫
Pero sí existe la opción de ser tu *novia de alquiler* 💑✨.

🌹 Podemos vernos personalmente y disfrutar de un momento agradable juntos:

💬 Conversaciones cercanas  
🥂 Acompañamiento especial  
💖 Experiencia auténtica conmigo
"""

MENSAJE_AYUDA = """💬 Hola amor 💕
Al hacer clic aquí estarás hablando directamente conmigo, la propietaria de Vela Noxx ✨.

⚠ IMPORTANTE ⚠
Para poder contestarte, NECESITO que me envíes tu @usuario de Telegram (ejemplo: @juan23, @carlitos89).

🚫 Si no me mandas tu @usuario, me sales como “usuario desconocido” 🤖❌ y no podré responderte. 

👉 Si no sabes cuál es tu usuario, créalo fácil en:
Configuración > Editar perfil > Nombre de usuario.
(Ejemplo: @pedro2025).

💞 Solo así podré contestarte de forma personalizada y especial 💌🥰
"""

# --- START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔑 Suscripción VIP", callback_data="vip")],
        [InlineKeyboardButton("🎁 Promociones", callback_data="promos")],
        [InlineKeyboardButton("💕 Salidas", callback_data="salidas")],
        [InlineKeyboardButton("💬 Hablar conmigo", callback_data="ayuda")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Verifica si es un mensaje nuevo o una edición (para evitar errores en la edición)
    if update.message:
        await update.message.reply_text(MENSAJE_BIENVENIDA, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=MENSAJE_BIENVENIDA, reply_markup=reply_markup, parse_mode="Markdown")


# --- BOTONES ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "vip":
        await query.message.reply_text(MENSAJE_VIP, parse_mode="Markdown")
        # Asegúrate de que el archivo 'qr_vip.jpeg' exista en la misma ruta de ejecución
        try:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=open("qr_vip.jpeg", "rb"))
        except FileNotFoundError:
            await query.message.reply_text("⚠️ Error: Archivo 'qr_vip.jpeg' no encontrado.")

    elif query.data == "promos":
        await query.message.reply_text(MENSAJE_PROMOS, parse_mode="Markdown")
        # Asegúrate de que el archivo 'qr_promo.jpeg' exista en la misma ruta de ejecución
        try:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=open("qr_promo.jpeg", "rb"))
        except FileNotFoundError:
            await query.message.reply_text("⚠️ Error: Archivo 'qr_promo.jpeg' no encontrado.")

    elif query.data == "salidas":
        await query.message.reply_text(MENSAJE_SALIDAS, parse_mode="Markdown")

    elif query.data == "ayuda":
        await query.message.reply_text(MENSAJE_AYUDA, parse_mode="Markdown")

# --- REENVÍO MEJORADO ---
async def reenvio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    # Se añade un ID para poder identificar al usuario en caso de querer responderle
    caption = f"💌 Mensaje de {user.first_name} (@{user.username or 'sin_username'}) - ID: {user.id}"

    # 1. Mensajes de Texto
    if update.message.text:
        mensaje = f"{caption}:\n\n{update.message.text}"
        await context.bot.send_message(ADMIN_ID, mensaje)

    # 2. Fotos
    elif update.message.photo:
        file = update.message.photo[-1].file_id
        await context.bot.send_photo(ADMIN_ID, file, caption=caption)

    # 3. Videos (¡AGREGADO!)
    elif update.message.video:
        file = update.message.video.file_id
        await context.bot.send_video(ADMIN_ID, file, caption=caption)

    # 4. Notas de Voz (¡AGREGADO!)
    elif update.message.voice:
        file = update.message.voice.file_id
        await context.bot.send_voice(ADMIN_ID, file, caption=caption)

    # 5. Documentos
    elif update.message.document:
        file = update.message.document.file_id
        await context.bot.send_document(ADMIN_ID, file, caption=caption)

    # 6. Cualquier otro tipo (Stickers, audios, etc.)
    else:
        # Esto notifica al administrador si se recibe un tipo de mensaje no cubierto explícitamente.
        mensaje = f"⚠️ Mensaje de tipo no cubierto (Ej. Sticker/Audio) de {caption}"
        await context.bot.send_message(ADMIN_ID, mensaje)


# --- MANEJO DE ERRORES ---
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Loggea los errores causados por Updates y los notifica."""
    # Imprime el error en los logs del hosting para diagnóstico
    print(f"⚠️ Update {update} causó el error {context.error}") 

    # Notifica al ADMIN_ID sobre el error si no es un error de conflicto (409)
    # El error 409 es manejo de infraestructura y no se notifica al admin
    if 'Conflict' not in str(context.error):
        try:
            await context.bot.send_message(ADMIN_ID, f"🚨 ERROR CRÍTICO DEL BOT:\n\n{context.error}")
        except Exception:
            # Si falla incluso enviar el error, simplemente se ignora y se loggea
            pass

# --- MAIN ---
def main():
    # El token se obtiene del entorno
    if not TOKEN:
        raise ValueError("La variable de entorno 'TOKEN' no está configurada.")
        
    app = Application.builder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    # Maneja todos los mensajes que NO son comandos y los envía a la función reenvio
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, reenvio)) 
    
    # Manejador de errores para hacer el bot más robusto
    app.add_error_handler(error_handler) 

    print("🤖 Bot en marcha...")
    app.run_polling()

if __name__ == "__main__":
    main()