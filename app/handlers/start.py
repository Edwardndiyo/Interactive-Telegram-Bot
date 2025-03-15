from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler

async def start(update: Update, context: CallbackContext):
    """Display main menu with options."""
    keyboard = [
        [InlineKeyboardButton("Search Product 🔍", callback_data="search_product"), 
         InlineKeyboardButton("Explore 🐛", callback_data="explore_product")],
        [InlineKeyboardButton("User Profile 👤", callback_data="profile"), 
         InlineKeyboardButton("Orders 📦", callback_data="orders")],
        [InlineKeyboardButton("AI Assistant 🤖", callback_data="ai_assistant"),
         InlineKeyboardButton("Quick Comparison ⚖️", callback_data="compare")]         
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Check if the update is from a CallbackQuery or a direct message
    if update.callback_query:
        # If triggered by a CallbackQuery (e.g., "Back to Main Menu" button)
        query = update.callback_query
        await query.answer()  # Acknowledge the callback
        await query.edit_message_text("Welcome to Deimr Stella! Please select an option:", reply_markup=reply_markup)
    else:
        # If triggered by a direct message (e.g., /start command)
        await update.message.reply_text("Welcome to Deimr Stella! Please select an option:", reply_markup=reply_markup)

# Register handlers
start_handler = CommandHandler("start", start)
main_menu_handler = CallbackQueryHandler(start, pattern="^main_menu$")