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



# down there works perfecrly, trying to implement number submission thingy



# from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
# from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler, MessageHandler, filters
# from app.utils.database import users_db

# # Helper function to normalize phone numbers
# def normalize_phone_number(phone_number):
#     """Normalize the phone number to ensure it starts with a '+'."""
#     if not phone_number.startswith("+"):
#         return f"+{phone_number}"
#     return phone_number

# async def start(update: Update, context: CallbackContext):
#     """Display main menu with options and handle phone number validation."""
#     # Check if the user has already shared their phone number
#     user_phone_number = context.user_data.get("phone_number")
#     if user_phone_number:
#         user_phone_number = normalize_phone_number(user_phone_number)  # Normalize the phone number
#     print(f"User phone number in context: {user_phone_number}")  # Debugging

#     if not user_phone_number:
#         # Prompt the user to share their phone number
#         keyboard = [[KeyboardButton("📞 Share My Number", request_contact=True)]]
#         reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
#         await update.message.reply_text(
#             "⚠️ You are not signed in on Deimr. Please share your phone number to proceed.",
#             reply_markup=reply_markup
#         )
#         return  # Exit the function to wait for the user's response

#     # Search for the user in the database using the normalized phone number
#     user_data = None
#     for user in users_db.values():
#         if user.get("phone_number") == user_phone_number:
#             user_data = user
#             break

#     if user_data:
#         # User is registered, fetch their name
#         user_name = user_data["name"]
#         welcome_message = f"Hello {user_name}! Welcome to Deimr Stella Seller’s Bot! 🎉"
#     else:
#         # User is not registered
#         welcome_message = "⚠️ You are not registered on Deimr. Please sign up on our website to access all bot's features."

#         # Create a button linking to the website
#         keyboard = [
#             [InlineKeyboardButton("Sign Up on Deimr", url="https://www.deimr.com/signup")]  # Replace with your website URL
#         ]
#         reply_markup = InlineKeyboardMarkup(keyboard)

#         # Send the welcome message with the sign-up button
#         await update.message.reply_text(welcome_message, reply_markup=reply_markup)
#         return  # Exit the function to prevent access to the main menu

#     # Main menu keyboard
#     keyboard = [
#         [InlineKeyboardButton("Messages", callback_data="messages"), 
#          InlineKeyboardButton("Orders 📦", callback_data="orders")],
#         [InlineKeyboardButton("AI Assistant 🤖", callback_data="ai_assistant")],
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)

#     # Check if the update is from a CallbackQuery or a direct message
#     if update.callback_query:
#         # If triggered by a CallbackQuery (e.g., "Back to Main Menu" button)
#         query = update.callback_query
#         await query.answer()  # Acknowledge the callback
#         await query.edit_message_text(welcome_message, reply_markup=reply_markup)
#     else:
#         # If triggered by a direct message (e.g., /start command)
#         await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# async def handle_contact(update: Update, context: CallbackContext):
#     """Handle the user's shared contact information."""
#     user_phone_number = update.message.contact.phone_number
#     normalized_phone_number = normalize_phone_number(user_phone_number)  # Normalize the phone number
#     print(f"User shared phone number: {user_phone_number} (Normalized: {normalized_phone_number})")  # Debugging
#     context.user_data["phone_number"] = normalized_phone_number  # Store the normalized phone number

#     # Search for the user in the database using the normalized phone number
#     user_data = None
#     for user in users_db.values():
#         if user.get("phone_number") == normalized_phone_number:
#             user_data = user
#             break

#     if user_data:
#         # User is registered, fetch their name
#         user_name = user_data["name"]
#         welcome_message = "You passed the test! Now you can enjoy the features in our bot seamlessly."
        
#         # Send the welcome message
#         await update.message.reply_text(welcome_message)

#         # Display the main menu
#         await start(update, context)
#     else:
#         # User is not registered
#         welcome_message = "⚠️ You are not registered on Deimr. Please sign up on our website to access all bot's features."

#         # Create a button linking to the website
#         keyboard = [
#             [InlineKeyboardButton("Sign Up on Deimr", url="https://www.deimr.com/signup")]  # Replace with your website URL
#         ]
#         reply_markup = InlineKeyboardMarkup(keyboard)

#         # Send the welcome message with the sign-up button
#         await update.message.reply_text(welcome_message, reply_markup=reply_markup)

#         # Do not display the main menu
#         return

# # Register handlers
# start_handler = CommandHandler("start", start)
# main_menu_handler = CallbackQueryHandler(start, pattern="^main_menu$")