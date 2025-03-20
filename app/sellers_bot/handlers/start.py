from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler

async def start(update: Update, context: CallbackContext):
    """Display main menu with options."""
     # Clear the state when returning to the main menu
    context.user_data.pop("state", None)

    keyboard = [
        [InlineKeyboardButton("Messages", callback_data="messages"), 
         InlineKeyboardButton("Orders 📦", callback_data="orders")],
        [InlineKeyboardButton("AI Assistant 🤖", callback_data="ai_assistant")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Check if the update is from a CallbackQuery or a direct message
    if update.callback_query:
        # If triggered by a CallbackQuery (e.g., "Back to Main Menu" button)
        query = update.callback_query
        await query.answer()  # Acknowledge the callback
        await query.edit_message_text(
            "Welcome to Deimr Stella Seller's Bot! Please select an option:",
            reply_markup=reply_markup
        )
    else:
        # If triggered by a direct message (e.g., /start command)
        await update.message.reply_text(
            "Welcome to Deimr Stella Seller's Bot! Please select an option:",
            reply_markup=reply_markup
        )

# Register handlers
start_handler = CommandHandler("start", start)
main_menu_handler = CallbackQueryHandler(start, pattern="^main_menu$")