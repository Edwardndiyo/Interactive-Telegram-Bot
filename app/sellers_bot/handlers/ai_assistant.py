from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CallbackQueryHandler

async def support(update: Update, context: CallbackContext):
    """Handle the Support button click."""
    print("Support function called!")  # Debugging
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        # Edit the existing message to display the AI Assistant screen
        await query.edit_message_text(
            "AI Assistant mode activated!\n"
            "🚧 Coming soon...\n\n",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
            ])
        )
    else:
        # If triggered by a direct message (e.g., /ai_assistant command)
        await update.message.reply_text(
            "AI Assistant mode activated!\n"
            "🚧 Coming soon...\n\n",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
            ])
        )

# Register handlers
support_handlers = [
    CallbackQueryHandler(support, pattern="^ai_assistant$"),
]