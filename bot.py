import os
import asyncio
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import config

# Build keyboard (uses InlineKeyboard in previous code; here keep same layout with callback data)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔑 Suscripción VIP", callback_data="vip")],
        [InlineKeyboardButton("🎁 Promociones", callback_data="promos")],
        [InlineKeyboardButton("💕 Salidas", callback_data="salidas")],
        [InlineKeyboardButton("💬 Hablar conmigo", callback_data="ayuda")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(config.MENSAJE_BIENVENIDA, reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "vip":
        await query.message.reply_text(config.MENSAJE_VIP, parse_mode="Markdown")
        qr_path = os.path.join("assets", config.QR_VIP)
        if os.path.exists(qr_path):
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=open(qr_path, "rb"))
    elif query.data == "promos":
        await query.message.reply_text(config.MENSAJE_PROMOS, parse_mode="Markdown")
        if config.PROMO_ACTIVA:
            qr_path = os.path.join("assets", config.QR_PROMO)
            if os.path.exists(qr_path):
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=open(qr_path, "rb"))
    elif query.data == "salidas":
        await query.message.reply_text(config.MENSAJE_SALIDAS, parse_mode="Markdown")
    elif query.data == "ayuda":
        await query.message.reply_text(config.MENSAJE_AYUDA, parse_mode="Markdown")

async def reenvio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    nombre = f"@{user.username}" if user.username else f"{user.first_name}"
    caption = f"💌 Mensaje de {user.first_name} ({nombre})"

    # Text messages
    if update.message.text:
        mensaje = f"{caption}:\n\n{update.message.text}"
        await context.bot.send_message(chat_id=config.ADMIN_ID, text=mensaje)

    # Photos
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        await context.bot.send_photo(chat_id=config.ADMIN_ID, photo=file_id, caption=caption)

    # Documents
    if update.message.document:
        file_id = update.message.document.file_id
        await context.bot.send_document(chat_id=config.ADMIN_ID, document=file_id, caption=caption)

async def main():
    # Create app
    app = ApplicationBuilder().token(config.TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, reenvio))

    # Set webhook
    domain = config.WEBHOOK_DOMAIN.rstrip("/")
    webhook_url = f"{domain}/webhook/{config.TOKEN}"

    print("🚀 Configurando webhook en:", webhook_url)
    await app.bot.set_webhook(webhook_url)

    # Run webhook server
    port = int(os.getenv("PORT", "8080"))
    await app.run_webhook(listen="0.0.0.0", port=port, url_path=f"webhook/{config.TOKEN}")

if __name__ == '__main__':
    asyncio.run(main())
