from telegram.ext import Application, CommandHandler
from telegram import Update, BotCommand

from app.sellers_bot.config import TOKEN



async def set_bot_commands(application):
    """Set a persistent 'Menu' button in the bot's command list."""
    commands = [
        BotCommand("menu", "Open the main menu"),  # Persistent button for menu
    ]
    await application.bot.set_my_commands(commands)

# Initialize the bot application
app = Application.builder().token(TOKEN).post_init(set_bot_commands).build()

async def start(update, context):
    await update.message.reply_text("Hello! I'm your bot.")

app.add_handler(CommandHandler("start", start))
