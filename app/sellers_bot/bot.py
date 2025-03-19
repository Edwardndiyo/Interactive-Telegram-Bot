from telegram.ext import Application, CommandHandler

app = Application.builder().token("7793244239:AAHzhaw2O2fwZH4HBxJMdyXqZYh__vxQaIA").build()

async def start(update, context):
    await update.message.reply_text("Hello! I'm your bot.")

app.add_handler(CommandHandler("start", start))
