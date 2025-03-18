from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CallbackQueryHandler

async def support(update: Update, context: CallbackContext):
    """Handle the Support button click."""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        message = query.message
    else:
        message = update.message

    # Display the AI Assistant message
    await message.reply_text(
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