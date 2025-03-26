from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
from telegram import Update, BotCommand
from app.sellers_bot.handlers.start import start, main_menu_handler
from app.sellers_bot.handlers.orders import orders_handlers
from app.sellers_bot.handlers.ai_assistant import support, support_handlers
from app.sellers_bot.handlers.messaging import messages_handlers  # Import the messages handlers
from app.sellers_bot.config import TOKEN
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
        from app.sellers_bot.handlers.orders import handle_message
        await handle_message(update, context)
    elif state and state.startswith("messages:"):
        from app.sellers_bot.handlers.messaging import handle_message
        await handle_message(update, context)
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

# Register the support handler
app.add_handler(CallbackQueryHandler(support, pattern="^ai_assistant$"))

# Register the main_menu handler
app.add_handler(main_menu_handler)  # Register the main_menu handler

# Register all handlers from orders.py
for handler in orders_handlers:
    app.add_handler(handler)

# Register all handlers from ai_assistant.py
for handler in support_handlers:
    app.add_handler(handler)

# Register all handlers from messaging.py
for handler in messages_handlers:  # Register the messages handlers
    app.add_handler(handler)

# Register the global message handler
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_global_message))

# Register the error handler
app.add_error_handler(error_handler)

if __name__ == "__main__":
    app.run_polling()






# Works well mostly, trying to implement the number grabing thing-  













# from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
# from telegram import Update, BotCommand
# from app.sellers_bot.handlers.start import start, main_menu_handler, handle_contact  # Import handle_contact
# from app.sellers_bot.handlers.orders import orders_handlers
# from app.sellers_bot.handlers.ai_assistant import support, support_handlers
# from app.sellers_bot.handlers.messaging import messages_handlers  # Import the messages handlers
# from app.sellers_bot.config import TOKEN
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Global message handler to dispatch messages based on state
# async def handle_global_message(update: Update, context: CallbackContext):
#     """Dispatch messages to the appropriate module based on the current state."""
#     state = context.user_data.get("state")
#     print(f"Current state: {state}")  # Debugging

#     if state and state.startswith("orders:"):
#         from app.sellers_bot.handlers.orders import handle_message
#         await handle_message(update, context)
#     elif state and state.startswith("messages:"):
#         from app.sellers_bot.handlers.messaging import handle_message
#         await handle_message(update, context)
#     else:
#         # If no valid state is found, call the unrecognized command handler
#         await handle_unrecognized_command(update, context)

# # Handler for unrecognized commands
# async def handle_unrecognized_command(update: Update, context: CallbackContext):
#     """Handles any unrecognized command and displays the main menu."""
#     menu_text = (
#         "⚠️ Sorry, I didn't understand that command.\n"
#         "Please choose from the menu below:"
#     )
    
#     # Send the main menu using the start function
#     await start(update, context)

# # Global error handler
# async def error_handler(update: Update, context: CallbackContext):
#     """Handles unexpected errors globally."""
#     logger.error(f"An error occurred: {context.error}")

#     error_message = (
#         "⚠️ Oops! Something went wrong.\n"
#         "Please try again later or select an option from the menu."
#     )
    
#     try:
#         await update.message.reply_text(error_message)
#     except Exception:
#         pass  # Avoid crashes if the error occurs outside a message context

# async def set_bot_commands(application: Application):
#     """Set a persistent 'Menu' button in the bot's command list."""
#     commands = [
#         BotCommand("start", "Start the bot"),
#         BotCommand("menu", "Open the main menu"),  # Persistent button for menu
#     ]
#     await application.bot.set_my_commands(commands)

# async def post_init(application: Application):
#     """Ensure bot commands are set after the bot starts."""
#     await set_bot_commands(application)

# # Initialize the bot application
# app = Application.builder().token(TOKEN).post_init(post_init).build()

# # Register the /start and /menu command handlers
# app.add_handler(CommandHandler("start", start))
# app.add_handler(CommandHandler("menu", start))  # Alias for the Menu button

# # Register the support handler
# app.add_handler(CallbackQueryHandler(support, pattern="^ai_assistant$"))

# # Register the main_menu handler
# app.add_handler(main_menu_handler)  # Register the main_menu handler

# # Register the contact handler for phone number sharing
# app.add_handler(MessageHandler(filters.CONTACT, handle_contact))  # Add this line

# # Register all handlers from orders.py
# for handler in orders_handlers:
#     app.add_handler(handler)

# # Register all handlers from ai_assistant.py
# for handler in support_handlers:
#     app.add_handler(handler)

# # Register all handlers from messaging.py
# for handler in messages_handlers:  # Register the messages handlers
#     app.add_handler(handler)

# # Register the global message handler
# app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_global_message))

# # Register the error handler
# app.add_error_handler(error_handler)

# if __name__ == "__main__":
#     app.run_polling()