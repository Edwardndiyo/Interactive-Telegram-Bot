from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CallbackContext, CommandHandler

async def start(update: Update, context: CallbackContext):
    """ Display main menu with options """
    keyboard = [
        [InlineKeyboardButton("Search Product 🔍", callback_data="search_product"), 
         InlineKeyboardButton("Orders 📦", callback_data="orders")],
        [InlineKeyboardButton("User Profile 👤", callback_data="profile"), 
         InlineKeyboardButton("Quick Comparison ⚖️", callback_data="compare")],
        [InlineKeyboardButton("AI Assistant 🤖", callback_data="ai_assistant")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to Deimr Stella! Please select an option:", reply_markup=reply_markup)

handler = CommandHandler("start", start)
