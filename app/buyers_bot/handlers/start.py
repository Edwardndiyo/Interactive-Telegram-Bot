# from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
# from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler

# async def start(update: Update, context: CallbackContext):
#     """Display main menu with options and clear any existing state."""
#     # Clear the state when returning to the main menu
#     context.user_data.pop("state", None)

#     keyboard = [
#         [InlineKeyboardButton("Search Product 🔍", callback_data="search_product"), 
#          InlineKeyboardButton("Explore 🐛", callback_data="explore_product")],
#         [InlineKeyboardButton("User Profile 👤", callback_data="profile"), 
#          InlineKeyboardButton("Orders 📦", callback_data="orders")],
#         [InlineKeyboardButton("AI Assistant 🤖", callback_data="ai_assistant"),
#          InlineKeyboardButton("Quick Comparison ⚖️", callback_data="compare_product")]         
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)

#     # Check if the update is from a CallbackQuery or a direct message
#     if update.callback_query:
#         # If triggered by a CallbackQuery (e.g., "Back to Main Menu" button)
#         query = update.callback_query
#         await query.answer()  # Acknowledge the callback
#         await query.edit_message_text("Welcome to Deimr Stella! Please select an option:", reply_markup=reply_markup)
#     else:
#         # If triggered by a direct message (e.g., /start command)
#         await update.message.reply_text("Welcome to Deimr Stella! Please select an option:", reply_markup=reply_markup)

# # Register handlers
# start_handler = CommandHandler("start", start)
# main_menu_handler = CallbackQueryHandler(start, pattern="^main_menu$")



# up here works perfectly implementing grabbing users number for verification - 



from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from app.utils.database import users_db

async def start(update: Update, context: CallbackContext):
    """Display main menu with options and handle phone number validation."""
    # Clear the state when returning to the main menu
    context.user_data.pop("state", None)

    # Check if the user has already shared their phone number
    user_phone_number = context.user_data.get("phone_number")
    print(f"User phone number in context: {user_phone_number}")  # Debugging

    # Search for the user in the database using the phone number
    user_data = None
    for user in users_db.values():
        if user.get("phone_number") == user_phone_number:
            user_data = user
            break

    if user_data:
        # User is registered, fetch their name
        user_name = user_data["name"]
        welcome_message = f"Hello {user_name}! Welcome to Deimr Stella Bot! 🎉"
    else:
        # User is not registered or hasn't shared their number
        welcome_message = "Welcome to Deimr Stella! Please share your phone number to proceed."

        if not user_phone_number:
            # Prompt the user to share their phone number
            keyboard = [[KeyboardButton("📞 Share My Number", request_contact=True)]]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            await update.message.reply_text(
                "⚠️ You are not signed in on Deimr. Please share your phone number to proceed.",
                reply_markup=reply_markup
            )
            return  # Exit the function to wait for the user's response

    # Main menu keyboard
    keyboard = [
        [InlineKeyboardButton("Search Product 🔍", callback_data="search_product"), 
         InlineKeyboardButton("Explore 🐛", callback_data="explore_product")],
        [InlineKeyboardButton("User Profile 👤", callback_data="profile"), 
         InlineKeyboardButton("Orders 📦", callback_data="orders")],
        [InlineKeyboardButton("AI Assistant 🤖", callback_data="ai_assistant"),
         InlineKeyboardButton("Quick Comparison ⚖️", callback_data="compare_product")]         
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Check if the update is from a CallbackQuery or a direct message
    if update.callback_query:
        # If triggered by a CallbackQuery (e.g., "Back to Main Menu" button)
        query = update.callback_query
        await query.answer()  # Acknowledge the callback
        await query.edit_message_text(welcome_message, reply_markup=reply_markup)
    else:
        # If triggered by a direct message (e.g., /start command)
        await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def handle_contact(update: Update, context: CallbackContext):
    """Handle the user's shared contact information."""
    user_phone_number = update.message.contact.phone_number
    print(f"User shared phone number: {user_phone_number}")  # Debugging
    context.user_data["phone_number"] = user_phone_number

    # Search for the user in the database using the phone number
    user_data = None
    for user in users_db.values():
        if user.get("phone_number") == user_phone_number:
            user_data = user
            break

    if user_data:
        # User is registered, fetch their name
        user_name = user_data["name"]
        welcome_message = f"You passed the test! Now you can enjoy the features in our bot seamlessly."
    else:
        # User is not registered
        welcome_message = "⚠️ You are not registered on Deimr. Please sign up on our website to access all bot's features."

        # Create a button linking to the website
        keyboard = [
            [InlineKeyboardButton("Sign Up on Deimr", url="https://www.deimr.com/signup")]  # Replace with your website URL
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send the welcome message with the sign-up button
        await update.message.reply_text(welcome_message, reply_markup=reply_markup)
        return  # Exit the function to prevent access to the main menu

    # Send the welcome message
    await update.message.reply_text(welcome_message)

    # Display the main menu
    await start(update, context)

# Register handlers
start_handler = CommandHandler("start", start)
main_menu_handler = CallbackQueryHandler(start, pattern="^main_menu$")

