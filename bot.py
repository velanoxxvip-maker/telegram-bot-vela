import os
import sys
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURACIÓN desde variables de entorno ---
TOKEN = os.environ.get("TOKEN")
ADMIN_ID = os.environ.get("ADMIN_ID")

if not TOKEN or not ADMIN_ID:
    print("❌ ERROR: Debes definir las variables de entorno TOKEN y ADMIN_ID")
    sys.exit(1)

try:
    ADMIN_ID = int(ADMIN_ID)
except ValueError:
    print("❌ ERROR: ADMIN_ID debe ser un número entero")
    sys.exit(1)

# --- MENSAJES ---
MENSAJE_BIENVENIDA = """🌟 Mensaje de bienvenida 🌟

👋 ¡Hola amor! Soy *Vela Noxx* 💋
Bienvenid@ a mi espacio exclusivo 🔥.

Explora el menú aquí abajo 👇 y descubre todo lo que tengo preparado para ti ✨.
"""

MENSAJE_VIP = """💎 *Suscripción VIP – Bs. 150 / mes* 💎

👉 Con tu suscripción tendrás acceso inmediato al *Canal VIP diamante* 💎, donde encontrarás:
✨ TODO mi contenido explícito🥵 y premium durante 1 mes completo.
🔥 Fotos + videos exclusivos.
💋 Acceso a lo más íntimo.
😈 Una experiencia única conmigo, sin censura.

📌 Acceso por 30 días al *Canal VIP DIAMANTE* con tu aporte de *Bs. 150*.
"""

MENSAJE_PROMOS = """💎 *Promoción Activa – Suscripción VIP* 💎

🔓 Acceso completo al *Canal VIP diamante* 💎 por *Bs. 100* todo el mes
🔥 Incluye mi mega contenido exclusivo:

✨ Lo más atrevido y diferente  
🌹 Todo en un solo lugar  
🚀 Con acceso inmediato  

📌 Aprovecha la promoción y disfruta de un mes completo de experiencias VIP.
"""

MENSAJE_SALIDAS = """🚫 *No realizo servicios* 🚫
Pero sí existe la opción de ser tu *novia de alquiler* 💑✨.

🌹 Podemos vernos personalmente y disfrutar de un momento agradable juntos:

💬 Conversaciones cercanas  
🥂 Acompañamiento especial  
💖 Experiencia auténtica conmigo
"""

MENSAJE_AYUDA = """📩 Escríbeme tu consulta aquí y yo la recibo directamente 💕
"""

# --- START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔑 Botón Suscripción VIP", callback_data="vip")],
        [InlineKeyboardButton("🎁 Botón Promociones", callback_data="promos")],
        [InlineKeyboardButton("💕 Botón Salidas", callback_data="salidas")],
        [InlineKeyboardButton("💬 Hablar conmigo", callback_data="ayuda")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(MENSAJE_BIENVENIDA, reply_markup=reply_markup, parse_mode="Markdown")

# --- BOTONES ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "vip":
        await query.message.reply_text(MENSAJE_VIP, parse_mode="Markdown")

    elif query.data == "promos":
        await query.message.reply_text(MENSAJE_PROMOS, parse_mode="Markdown")

    elif query.data == "salidas":
        await query.message.reply_text(MENSAJE_SALIDAS, parse_mode="Markdown")

    elif query.data == "ayuda":
        await query.message.reply_text(MENSAJE_AYUDA, parse_mode="Markdown")

# --- REENVÍO DE MENSAJES, IMÁGENES Y DOCUMENTOS ---
async def reenvio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    caption = f"💌 Mensaje de {user.first_name} (@{user.username or 'sin_username'})"

    # --- Texto ---
    if update.message.text:
        mensaje = f"{caption}:\n\n{update.message.text}"
        await context.bot.send_message(ADMIN_ID, mensaje)

    # --- Foto ---
    elif update.message.photo:
        file = update.message.photo[-1].file_id
        await context.bot.send_photo(ADMIN_ID, file, caption=caption)

    # --- Documento ---
    elif update.message.document:
        file = update.message.document.file_id
        await context.bot.send_document(ADMIN_ID, file, caption=caption)

# --- MAIN ---
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, reenvio))

    print("🤖 Bot en marcha...")
    app.run_polling()

if __name__ == "__main__":
    main()
