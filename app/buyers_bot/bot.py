from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
from app.buyers_bot.config import TOKEN
from app.buyers_bot.handlers.start import start  #,start_handlers  # Import the start function
from app.buyers_bot.handlers.explore import explore_product, explore_handlers
from app.buyers_bot.handlers.search import search_product, search_handlers
from app.buyers_bot.handlers.orders import orders_handlers
from app.buyers_bot.handlers.profile import profile_handlers
from app.buyers_bot.handlers.compare import compare_product, compare_handlers
from app.buyers_bot.handlers.ai_assistant import support, support_handlers 
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global message handler to dispatch messages based on state
async def handle_global_message(update: Update, context: CallbackContext):
    """Dispatch messages to the appropriate module based on the current state."""
    state = context.user_data.get("state")
    print(f"Current state: {state}")  # Debugging

    if state and state.startswith("orders:"):
        from app.buyers_bot.handlers.orders import handle_message
        await handle_message(update, context)
    elif state and state.startswith("search:"):
        from app.buyers_bot.handlers.search import handle_product_name
        await handle_product_name(update, context)
    elif state and state.startswith("profile:"):
        from app.buyers_bot.handlers.profile import handle_profile_message
        await handle_profile_message(update, context)
    elif state and state.startswith("compare:"):
        from app.buyers_bot.handlers.compare import handle_product_input
        await handle_product_input(update, context)
    # elif state and state.startswith("start:"):
    #     from handlers.start import handle_phone_input
    #     await handle_phone_input(update, context)
    else:
        # If no valid state is found, call the unrecognized command handler
        await handle_unrecognized_command(update, context)

# Handler for unrecognized commands
async def handle_unrecognized_command(update: Update, context: CallbackContext):
    """Handles any unrecognized command and displays the main menu."""
    menu_text = (
        "⚠️ Sorry, I didn't understand that command.\n"
        "Please choose from the menu below:"
    )
    
    # Send the main menu using the start function
    await start(update, context)

# Global error handler
async def error_handler(update: Update, context: CallbackContext):
    """Handles unexpected errors globally."""
    logger.error(f"An error occurred: {context.error}")

    error_message = (
        "⚠️ Oops! Something went wrong.\n"
        "Please try again later or select an option from the menu."
    )
    
    try:
        await update.message.reply_text(error_message)
    except Exception:
        pass  # Avoid crashes if the error occurs outside a message context

async def set_bot_commands(application):
    """Set a persistent 'Menu' button in the bot's command list."""
    commands = [
        BotCommand("menu", "Open the main menu"),  # Persistent button for menu
    ]
    await application.bot.set_my_commands(commands)

# Initialize the bot application
app = Application.builder().token(TOKEN).post_init(set_bot_commands).build()

# Register the /start and /menu command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("menu", start))  # Alias for the Menu button

# Register the explore_product handler
app.add_handler(CallbackQueryHandler(explore_product, pattern="^explore_product$"))

# Register the search_product handler
app.add_handler(CallbackQueryHandler(search_product, pattern="^search_product$"))

# Register the compare_product handler
app.add_handler(CallbackQueryHandler(compare_product, pattern="^compare_product$"))

# Register the support handler
app.add_handler(CallbackQueryHandler(support, pattern="^ai_assistant$"))

# Register all handlers from explore.py
for handler in explore_handlers:
    app.add_handler(handler)

# Register all handlers from orders.py
for handler in orders_handlers:
    app.add_handler(handler)

# Register all handlers from search.py
for handler in search_handlers:
    app.add_handler(handler)

# Register all handlers from profile.py
for handler in profile_handlers:
    app.add_handler(handler)

# Register all handlers from compare.py
for handler in compare_handlers:
    app.add_handler(handler)

# Register all handlers from ai_assistant.py
for handler in support_handlers:
    app.add_handler(handler)

# register start handlers
# for handler in start_handlers:
#     app.add_handler(handler)

# Register the global message handler
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_global_message))

# Register the error handler
app.add_error_handler(error_handler)

# Run the bot
if __name__ == "__main__":
    app.run_polling()
